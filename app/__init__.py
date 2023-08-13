from flask import Flask 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config 
from sqlalchemy import MetaData
import datetime # 오늘 날짜대로 로그 파일 수집을 위한 시간 모듈 import

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

    import logging.config

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")  
    if not app.debug: 
        # 즉 debug=true면 이는 false로서 아래 코드를 읽어옵니다.
        # 실제 상용화단계에서 로깅을 진행하라는 의미입니다.
            import logging

            logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {  # 로그 출력 패턴 1
                    'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                    'style': '{',
                },
                'simple': { # 로그 출력 패턴 2
                    'format': '{levelname} {message}',
                    'style': '{',
                },
            },
            'handlers': {
                'console': { # 콘솔에 출력하는 로그의 범위
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
                'file': {
                    'level': 'DEBUG',
                    'encoding': 'utf-8',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': app.root_path + f'/logs/{today_date}-mysiteLog.log', # 이 파일에 로그를 수집할 예정
                    'formatter': 'verbose', # 적용시킨 로그 출력 패턴 1대로 수집
                    'maxBytes': 1024*1024*5, # 5 MB
                    'backupCount': 5,
                },
                'errors': { # 에러가 난 경우 별도 파일로 수집할 예정
                    'level': 'ERROR',
                    'encoding': 'utf-8',
                    'class': 'logging.FileHandler',
                    'filename': app.root_path + f'/logs/{today_date}-mysiteErrorLog.log',
                    'formatter': 'simple', # 로그 출력 패턴 2대로 수집
                },
            },
            'loggers': {
                'flask.app': {  
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
                'flask.request': {
                    'handlers': ['errors'],
                    'level': 'ERROR',
                    'propagate': True,
                },
                'my': {
                    'handlers': ['console', 'file', 'errors'],
                    'level': 'INFO',
                },
            },
        })

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