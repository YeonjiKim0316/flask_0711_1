from flask import Blueprint, render_template, redirect
from app.models import Question, Answer
from datetime import datetime
from app import db
from app.forms import QuestionForm, AnswerForm


# 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소
question = Blueprint('question', __name__, url_prefix='/question')

@question.route('/detail/<int:question_id>/')
def detail(question_id):
    # AnswerForm을 추가합니다
    form = AnswerForm()
    # question = Question.query.get(question_id)
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# view에서 주소창에 쓸 uri를 만들때는 /1 /2 /3 
@question.route('/list/')
def post_list():
    question_list = Question.query.all()
    return render_template('question/question_list.html', question_list=question_list) 

@question.route('/create', methods=['GET', 'POST'])
def create():
    # 입력양식에 데이터를 입력 받는다
    form = QuestionForm()
    # 로그인 한 경우, 로그인 하지 않은 경우
    # 데이터가 요구조건에 맞춰서 모두 잘 들어와있는지 
    if form.validate_on_submit():
        q = Question(subject=form.subject.data, content=form.content.data,     
                     create_date=datetime.now())
        db.session.add(q)
        db.session.commit()
        return redirect('/success')
    return render_template('question/question_form.html', form=form)

@question.route('/success')
def success():
    question_list = Question.query.all()
    return render_template('question/question_list.html', question_list=question_list) 


