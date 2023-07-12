from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
                       # label, 데이터를 보내기 위한 제약조건
    subject = StringField('제목', validators=[DataRequired()])
    content = TextAreaField('내용', validators=[DataRequired()])

class AnswerForm(FlaskForm):
    content = TextAreaField('답변 내용', validators=[DataRequired()])