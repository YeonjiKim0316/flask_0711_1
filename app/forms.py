from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class QuestionForm(FlaskForm):
                       # label, 데이터를 보내기 위한 제약조건
    subject = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])

class AnswerForm(FlaskForm):
    content = TextAreaField('답변 내용', validators=[DataRequired()])

class UserCreateForm(FlaskForm):
    username = StringField("사용자ID", validators=[DataRequired(), Length(5, 15, "5글자 이상 15글자 이내로 입력해주세요")])
    password1 = StringField("비밀번호", validators=[DataRequired(), EqualTo('password2', "비밀번호가 틀립니다")])
    password2 = StringField("비밀번호 다시 입력", validators=[DataRequired()])
    email = StringField("이메일", validators=[DataRequired()])