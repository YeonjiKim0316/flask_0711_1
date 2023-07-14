from flask import Flask 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config 
from sqlalchemy import MetaData


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ORM에 대한 설정
    app.config.from_object(config)
    db.init_app(app)
    # migrate.init_app(app, db)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from .views import basic_views, answer_views, question_views, auth_views
    app.register_blueprint(basic_views.fisa)
    app.register_blueprint(answer_views.answer)
    app.register_blueprint(question_views.question)
    app.register_blueprint(auth_views.auth)
    
    from .filter import format_datetime, format_datetime2
    app.jinja_env.filters['date_time'] = format_datetime
    app.jinja_env.filters['date_time2'] = format_datetime2
    return app