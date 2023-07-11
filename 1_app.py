from flask import Flask 

# 따로 set FLASK_APP=-파일명 적어주지 않으면 app.py를 기본 실행 입구로 찾습니다
app = Flask(__name__)

print(__name__)

@app.route('/about_me')
def about_me():
    return f'저는 {__name__} 입니다' 

@app.route('/hello')
def hello():
    return f'안녕하세요' 

@app.route('/bye')
def bye():
    return f'잘 가세요 ' 