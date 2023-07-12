from flask import Blueprint, render_template, redirect
from app.models import Question, Answer
# 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소
fisa = Blueprint('basic', __name__, url_prefix='/')

@fisa.route('/detail/<int:question_id>/')
def detail(question_id):
    # question = Question.query.get(question_id)
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)

@fisa.route('/list')
def post_list():
    question_list = Question.query.all()
    return render_template('question/question_list.html', question_list=question_list) 


# /loop 라는 uri로 이동하는 화면을 만듭니다. 
# test.html 파일로 가게 됩니다. test = [ 1, 2, 3, 4, 5] 라는 리스트를 같이 return 합니다. 
@fisa.route('/loop')
def loop():
    test = [ 1, 2, 3, 4, 5]
    return render_template('test.html', list=test)

@fisa.route('/')
def index():
    return render_template('index.html')

@fisa.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)