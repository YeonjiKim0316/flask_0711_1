from flask import Blueprint, render_template, redirect
from app.models import Question, Answer
from datetime import datetime
from app import db
from app.forms import QuestionForm, AnswerForm

# log를 위한 모듈 추가
import logging

# 로거 추가
# logger = logging.getLogger('flask.app')
logger = logging.getLogger('my')  # my 세팅 상태로 변경해보기

# 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소
fisa = Blueprint('basic', __name__, url_prefix='/')


@fisa.route('/')
def index():

    logger.info('INFO 레벨의 메시지 기록 확인')
    logger.warning('WARNING 레벨의 메시지 기록 확인')
    logger.error('ERROR 레벨의 메시지 기록 확인')
    return render_template('index.html')


