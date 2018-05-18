# coding: utf-8
#! /usr/bin/env python

"""Some Tools"""

import shutil
import datetime
import db
import csv


def backup_db():
    """Backup Cards"""
    bak_time = datetime.datetime.now()
    bak_dir = "./bak/" + bak_time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    bak_file = bak_dir + bak_time.strftime("%Y-%m-%d-%H-%M-%S") + ".db"
    bak_mdfile = bak_dir + bak_time.strftime("%Y-%m-%d-%H-%M-%S") + ".md"
    shutil.copytree("./static/cards", bak_dir)
    shutil.copyfile("FlashCards.md", bak_mdfile)
    shutil.copyfile("cards.db", bak_file)


def export_cards(db_path):
    txt = """---
title: FlashCards
documentclass: ctexart
...

"""
    con = db.connect_db(db_path)
    cur = con.cursor()
    sql = """SELECT id, question, answer,
             cdate, efactor, revdate
             FROM cards
             ORDER BY id"""
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    for row in rows:
        title = "\n# " + str(row[0]) + ":" + \
                str(row[3]) + "~" + str(row[5]) + ": " + str(row[4]) + "\n\n"
        question = row[1] + "\n"
        answer = row[2] + "\n"
        txt += title + question + "\n\n-----\n\n" + answer
    txt = txt.encode('utf-8')
    txt = txt.replace("/static/cards/", "./static/cards/")
    with open('FlashCards.md', "w") as fil:
        fil.write(txt)
    return


def add_log(card, quality):
    now_time = datetime.datetime.now()
    log_time = now_time.strftime("%Y-%m-%d-%H-%M-%S")
    logfile = "./log/log" + now_time.strftime("%Y-%m") + ".csv"
    with open(logfile, "a") as fil:
        csvfil = csv.writer(fil)
        csvfil.writerow([card['id'],
                         log_time,
                         quality,
                         card['cdate'],
                         card['efactor'],
                         card['reps'],
                         card['inter'],
                         card['revdate'],
                         card['trials'],
                         card['quality']])
