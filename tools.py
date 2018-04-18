# coding: utf-8
#! /usr/bin/env python

"""Some Tools"""

import shutil
import datetime


def backup_db():
    """Backup Cards"""
    bak_time = datetime.datetime.now()
    bak_dir = "./bak/" + bak_time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    bak_file = bak_dir + bak_time.strftime("%Y-%m-%d-%H-%M-%S") + ".db"
    shutil.copytree("./static/cards", bak_dir)
    shutil.copyfile("cards.db", bak_file)
