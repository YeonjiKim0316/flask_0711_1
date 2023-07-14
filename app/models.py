from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))

class Answer(db.Model):
    # 답변의 고유번호 - 숫자 PK다 : 다음번호 자동 생성
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    # question 과 관련된 객체에서 어느 답변들이 question에 딸려오는지를 'answer_set'이라는 필드로 가져올 수 있게 추가한 기능
    question = db.relationship('Question', backref=db.backref('answer_set'))
    # Foreign Key로 걸려있는 테이블에서 삭제가 발생했을 때 
            # 1) Answer도 같이 지운다
            # 2) Answer는 남겨놓는다 
                # Question의 id를 남겨놓는다
                # Question의 id를 삭제한다
    # 비어있는 댓글 user_id에 1번 회원의 정보를 채워넣음
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True, server_default="1")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)   
    user = db.relationship('User', backref=db.backref('answer_set'))

class User(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)