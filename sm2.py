# coding: utf-8
#! /usr/bin/env python

"""SuperMemo 2.0
https://www.supermemo.com/english/ol/sm2.htm
"""

import math
from datetime import datetime, date, timedelta


def check_card(card):
    """A flashcard is a dictionary that contains `require_keys`"""
    require_keys = ['cdate',
                    'efactor',
                    'reps',
                    'inter',
                    'revdate',
                    'trials',
                    'quality']
    assert set(require_keys) <= set(card.keys())
    assert isinstance(card['cdate'], date)
    assert isinstance(card['revdate'], date)
    assert 1.3 <= card['efactor'] <= 2.5
    assert 0 <= card['quality'] <= 5


def update_efactor(card, quality):
    """ Update E-Factor

        Easiness factor(E-Factor) reflecting the easiness of memorizing
        and retaining a given item in memory.
    """
    check_card(card)

    efactor = card['efactor']
    hardest = 1.3
    easiest = 2.5

    new_ef = (efactor - 0.8 + 0.28 * quality
              - 0.02 * quality * quality)

    if new_ef < hardest:
        card['efactor'] = hardest
    elif new_ef > easiest:
        card['efactor'] = easiest
    else:
        card['efactor'] = new_ef

    return


def review(card, quality):
    """Review Card"""
    check_card(card)
    update_efactor(card, quality)
    if quality < 3:
        card.update({'cdate': date.today(),
                     'revdate': date.today(),
                     'reps': 0,
                     'inter': 0,
                     'trials': 0,
                     'quality': 0})
    else:
        card['reps'] += 1
        reps = card['reps']
        if reps == 1:
            card['inter'] = 1
        elif reps == 2:
            card['inter'] = 6
        else:
            card['inter'] = card['inter'] * card['efactor']

    card['trials'] = 0
    card['quality'] = 0
    card['revdate'] = card['cdate'] + timedelta(days=math.ceil(card['inter']))
    return


def trial(card, quality):
    """It took three successful trials to complete a review"""
    check_card(card)
    assert quality in (0, 1, 2, 3, 4, 5)

    if quality < 3:
        review(card, quality)
    else:
        card['trials'] += 1
        card['quality'] += float(quality) / 2
    if card['trials'] >= 2:
        review(card, card['quality'])
    return


def create_card():
    """Return a card created today"""
    card = {'cdate': date.today(),
            'efactor': 2.5,
            'reps': 0,
            'inter': 0,
            'revdate': date.today(),
            'trials': 0,
            'quality': 0}
    return card
