from flask import Flask 

def create_app():
    app = Flask(__name__)

    from .views import basic_views, yeonji_views
    app.register_blueprint(basic_views.fisa)
    app.register_blueprint(yeonji_views.yeonji)
    return app