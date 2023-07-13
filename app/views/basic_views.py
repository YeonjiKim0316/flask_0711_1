from flask import Blueprint, render_template, redirect
from app.models import Question, Answer
from datetime import datetime
from app import db
from app.forms import QuestionForm, AnswerForm


# 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소
fisa = Blueprint('basic', __name__, url_prefix='/')

@fisa.route('/')
def index():
    return render_template('index.html')


