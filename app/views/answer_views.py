from flask import Blueprint, render_template, request, g, url_for, redirect, flash
from app.forms import AnswerForm
from app import db
from app.models import Answer, Question
from datetime import datetime
from werkzeug.utils import redirect
from app.views.auth_views import login_required


answer = Blueprint('answer', __name__, url_prefix='/answer')

# 작성과 수정을 하나의 폼에서 사용할 예정입니다.
@answer.route('/create/<int:question_id>/', methods=['POST'])
@login_required
def create(question_id):
    form = AnswerForm()
    # question 화면 가져오기
    question = Question.query.get_or_404(question_id)
    # question = Question.query.all(question_id)
    if form.validate_on_submit():
        # 어느 글에서 오는지 (question_id)
        # content = request.form['content']
        a = Answer(content=form.content.data, create_date=datetime.now(), user=g.user)

        # answer의 question_id 필드에 추가
        # answer_set은 model에 정의한 답변에서 글을 끌어오기위한 backref의 객체명입니다.
        question.answer_set.append(a)
        db.session.add(a)
        db.session.commit()
        # question으로 불리우는 basic_views.py의 detail 함수를 호출하는데 question_id를 함께 전달
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)


@answer.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)

@answer.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))