# coding: utf-8
#! /usr/bin/env python

"""Card"""

import db
import sm2
from markdown import markdown
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard gust'
bootstrap = Bootstrap(app)
db_path = "cards.db"


class QAForm(FlaskForm):
    question = TextAreaField('Q', validators=[DataRequired()],
                             render_kw={"rows": 10, "cols": 10})
    answer = TextAreaField('A', validators=[DataRequired()],
                           render_kw={"rows": 10, "cols": 10})
    submit = SubmitField(u'add')


class LearnForm(FlaskForm):
    quality = RadioField('Grade',
                         choices=[('0', '0'), ('1', '1'), ('2', '2'),
                                  ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField(u'YES')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = QAForm()
    if form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        db.add_card(question, answer, db_path)
        return redirect(url_for('add'))
    return render_template('add.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def learn():
    card = db.get_card(db_path)
    if card is None:
        return render_template('NoCard.html')
    question = markdown(card['question'], ['extra'])
    answer = markdown(card['answer'], ['extra'])
    form = LearnForm()
    if form.validate_on_submit():
        quality = int(form.quality.data)
        sm2.trial(card, quality)
        db.update_card(card, db_path)
        return redirect(url_for('learn'))
    return render_template('learn.html',
                           question=question,
                           answer=answer,
                           form=form)


if __name__ == '__main__':
    app.run(debug=True)
