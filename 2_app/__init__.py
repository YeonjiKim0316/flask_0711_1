from flask import Flask 

def create_app():
    app = Flask(__name__)

    @app.route('/about_me')
    def about_me():
        return f'저는 {__name__} 입니다' 

    @app.route('/hello')
    def hello():
        return f'안녕하세요' 

    @app.route('/bye')
    def bye():
        return f'잘 가세요 ' 
    
    return app