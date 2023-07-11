from flask import Blueprint
from app.models import Question, Answer

                 # 우리가 부를 이름, flask 프레임워크가 찾을 이름, 라우팅주소
fisa = Blueprint('basic', __name__, url_prefix='/fisa')

@fisa.route('/about_me')
def about_me():
    return f'저는 {__name__} 입니다' 

@fisa.route('/hello')
def hello():
    return f'안녕하세요' 

@fisa.route('/bye')
def bye():
    return f'잘 가세요 ' 

