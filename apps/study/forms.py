from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class WriteForm(FlaskForm):
  subject = StringField(
    "글제목",
    validators=[
      DataRequired('제목은 필수 입력입니다.')
    ]
  )
  content = TextAreaField(
    "내용",
    validators=[
      DataRequired('내용은 필수입력입니다.')
    ]
  )
  writer = StringField(
    "작성자",
    validators=[
      DataRequired('작성자는 필수입력')
    ]
  )
  submit = SubmitField('글등록')
