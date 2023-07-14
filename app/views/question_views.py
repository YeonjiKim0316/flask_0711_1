from flask import Blueprint, render_template, request, g, url_for, redirect, flash
from app.models import Question, Answer
from datetime import datetime
from app import db
from app.forms import QuestionForm, AnswerForm
from app.views.auth_views import login_required

# 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소
question = Blueprint('question', __name__, url_prefix='/question')

@question.route('/detail/<int:question_id>/')
def detail(question_id):
    # AnswerForm을 추가합니다
    form = AnswerForm()
    # question = Question.query.get(question_id)
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# pagenation으로 글 목록 출력하기
@question.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
     # 시간순으로 최신글을 맨 위로 올릴 것인지
    question_list = Question.query.order_by(Question.create_date.desc())
    # 10개씩 끊어서 출력 
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)


@question.route('/create/', methods=('GET', 'POST'))
@login_required # 접근 권한을 확인하기 위한 데코러이터 
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('basic.index'))
    return render_template('question/question_form.html', form=form)


@question.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@question.route('/delete/<int:question_id>')
@login_required # 로그인이 안 되어 있으면 auth.login 으로 GET 방식으로 이동
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question.detail'))