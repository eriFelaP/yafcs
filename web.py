# coding: utf-8
#! /usr/bin/env python

"""Card"""

import db
import sm2
import tools
from markdown import markdown
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard gust'
db_path = "cards.db"
manager = Manager(app)
card = db.get_card(db_path)  # global

tools.export_cards(db_path)
tools.backup_db()


class QAForm(FlaskForm):
    question = TextAreaField('Q', validators=[DataRequired()],
                             render_kw={"rows": 10, "cols": 10})
    answer = TextAreaField('A', validators=[DataRequired()],
                           render_kw={"rows": 10, "cols": 10})
    note = TextAreaField('N', validators=[DataRequired()],
                          render_kw={"rows": 1, "cols": 10})
    submit = SubmitField(u'add')


class LearnForm(FlaskForm):
    submit0 = SubmitField('0 blackout')
    submit1 = SubmitField('1 incorrect')
    submit2 = SubmitField('2 incorrect')
    submit3 = SubmitField('3 correct')
    submit4 = SubmitField('4 correct')
    submit5 = SubmitField('5 perfect')
    submit6 = SubmitField('DELETE')
    submit7 = SubmitField('EDIT')
    submit8 = SubmitField('NOTE')


@app.route('/add/', methods=['GET', 'POST'])
def add():
    global card
    form = QAForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        note = form.note.data
        message = db.add_card(question, answer,note, db_path)
        if message is not None:
            flash(message)
        card = db.get_card(db_path)
        return redirect(url_for('add'))
    else:
        form.note.data = 'default'
    return render_template('add.html', form=form)


@app.route('/edit/', methods=['GET', 'POST'])
def edit():
    global card
    form = QAForm()
    if form.validate_on_submit():
        card['question'] = form.question.data
        card['answer'] = form.answer.data
        card['note'] = form.note.data
        message = db.update_card(card, db_path)
        if message is not None:
            flash(message)
            card = db.get_card(db_path)
        return redirect(url_for('learn'))
    else:
        form.question.data = card['question']
        form.answer.data = card['answer']
        form.note.data = card['note']
    return render_template('add.html', form=form)


@app.route('/statistics/', methods=['GET', 'POST'])
def statistics():
    today_cards, all_cards = db.statistics_cards(db_path)
    return render_template('statistics.html',
                           today_cards=today_cards,
                           all_cards=all_cards)


@app.route('/', methods=['GET', 'POST'])
def learn():
    global card
    if card is None:
        return render_template('NoCard.html')
    question = markdown(card['question'], ['extra'])
    answer = markdown(card['answer'], ['extra'])
    form = LearnForm()
    if form.validate_on_submit():
        if form.submit0.data:
            quality = 0
        elif form.submit1.data:
            quality = 1
        elif form.submit2.data:
            quality = 2
        elif form.submit3.data:
            quality = 3
        elif form.submit4.data:
            quality = 4
        elif form.submit5.data:
            quality = 5
        elif form.submit6.data:
            db.delete_card(card, db_path)
            card = db.get_card(db_path)
            return redirect(url_for('learn'))
        elif form.submit7.data:
            return redirect(url_for('edit'))
        elif form.submit8.data:
            return redirect(url_for('note'))
        else:
            pass
        sm2.trial(card, quality)
        db.update_card(card, db_path)
        tools.add_log(card, quality)
        card = db.get_card(db_path)
        return redirect(url_for('learn'))
    return render_template('learn.html',
                           question=question,
                           answer=answer,
                           form=form)

@app.route('/note/', methods=['GET', 'POST'])
def note():
    global card
    note_path = "./note/" + card['note'] + ".md"
    with open(note_path) as fil:
        content = fil.read()
        content = content.decode('utf-8')
        note_content = markdown(content, ['extra'])
    return render_template('note.html',
                           note_content = note_content)

if __name__ == '__main__':
    manager.run()
