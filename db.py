# coding: utf-8
#! /usr/bin/env python

"""Store flashcards in the database."""

import sqlite3
from datetime import datetime
import random
import os
from sm2 import trial, create_card


def execute_sql_script(database, sqlscript):
    """Execute SQL script in sqlite3 database"""
    with open(sqlscript) as script:
        sql = "".join(script.readlines())
        cur = database.cursor()
        cur.executescript(sql)
        database.commit()


def connect_db(path):
    """If database exists, connect database, else create database"""
    createscript = "create.sql"
    if os.path.exists(path):
        database = sqlite3.connect(path)
    else:
        database = sqlite3.connect(path)
        execute_sql_script(database, createscript)
    return database


def add_card(question, answer,note, db_path):
    """Add a card into sqlite3 database"""
    card = create_card()
    card['question'] = question
    card['answer'] = answer
    card['note'] = note

    con = connect_db(db_path)
    cur = con.cursor()
    header = tuple(card.keys())
    row = tuple([card[key] for key in header])
    sql = 'INSERT INTO cards ({0}) VALUES ({1});'.format(
        ",".join(header),
        ",".join(["?"] * len(header)))
    try:
        cur.execute(sql, row)
        con.commit()
        con.close()
    except sqlite3.IntegrityError as error:
        con.close()
        print(error)
        return "The insert data is duplicated."
    except sqlite3.OperationalError as error:
        con.close()
        print(error)
        return "Database occupied"
    return


def update_card(card, db_path):
    """Update card to database"""
    database = connect_db(db_path)
    cur = database.cursor()
    sql = """UPDATE cards SET question=?,answer=?, cdate=?,efactor=?,
             reps=?, inter=?,revdate=?,trials=?,quality=?, note=? WHERE id = ?"""
    try:
        cur.execute(sql, (card['question'],
                          card['answer'],
                          card['cdate'],
                          card['efactor'],
                          card['reps'],
                          card['inter'],
                          card['revdate'],
                          card['trials'],
                          card['quality'],
                          card['note'],
                          card['id']))
        database.commit()
        database.close()
    except sqlite3.IntegrityError as error:
        database.close()
        print(error)
        return "The insert data is duplicated."
    except sqlite3.OperationalError as error:
        database.close()
        print(error)
        return "Database occupied"
    return


def get_card(db_path):
    """Get the card to review"""
    sql = """SELECT id, question, answer, cdate, efactor,
             reps, inter, revdate, trials, quality, "note"
             FROM cards
             WHERE julianday(revdate) <= julianday('now')
             ORDER BY random() limit 1"""
    database = connect_db(db_path)
    cur = database.cursor()
    cur.execute(sql)
    header = ("id", "question", "answer", "cdate", "efactor",
              "reps", "inter", "revdate", "trials", "quality", "note")
    row = cur.fetchone()
    if row is None:
        return None
    card = dict(list(zip(header, row)))
    card['cdate'] = datetime.strptime(card['cdate'], "%Y-%m-%d").date()
    card['revdate'] = datetime.strptime(card['revdate'], "%Y-%m-%d").date()
    database.close()
    return card


def delete_card(card, db_path):
    database = connect_db(db_path)
    cur = database.cursor()
    cur.execute('DELETE FROM cards WHERE id =?;', (card['id'],))
    database.commit()
    database.close()


def statistics_cards(db_path):
    database = connect_db(db_path)
    cur = database.cursor()
    cur.execute(
        "SELECT Count(*) FROM cards WHERE julianday(revdate) <= julianday('now')")
    today_cards = cur.fetchone()[0]
    cur.execute(
        "SELECT Count(*) FROM cards")
    all_cards = cur.fetchone()[0]
    database.commit()
    database.close()
    return today_cards, all_cards
