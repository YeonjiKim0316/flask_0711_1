import os
from dotenv import load_dotenv

# load .env
load_dotenv()

myDBid = os.environ.get('DBid')
myDBpw = os.environ.get('DBpassword')
mySecretKey = os.environ.get('FLASK_SECRET_KEY')

# db를 저장할 폴더/파일이름 
BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'test.db'))
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{myDBid}:{myDBpw}@yeonji-aws-db.cuhrebejg4k4.ap-northeast-2.rds.amazonaws.com:3306/qna"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY= mySecretKey

# 또한 디버그모드를 False로 주고 ALLOWED_HOSTS를 '*'로 변경해줍니다.
DEBUG = False
ALLOWED_HOSTS = ['*']