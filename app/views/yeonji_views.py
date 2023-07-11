from flask import Blueprint

yeonji = Blueprint('yeonji', __name__, url_prefix='/yeonji')

@yeonji.route('/about_me')
def about_me():
    return f'저는 {__name__} 입니다' 

@yeonji.route('/hello')
def hello():
    return f'안녕하세요' 

@yeonji.route('/bye')
def bye():
    return f'잘 가세요 ' 