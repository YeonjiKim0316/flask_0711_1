from flask import Flask 

def create_app():
    app = Flask(__name__)

    from .views import basic_views
    app.register_blueprint(basic_views.fisa)
    
    return app