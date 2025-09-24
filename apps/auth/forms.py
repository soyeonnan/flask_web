from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
  username = StringField(
    "사용자명",
    validators=[
      DataRequired('사용자명 필수 입력'),
      Length(3,20,"3~30자 이내로 입력")
    ]
  )
  email = EmailField(
    "메일주소",
    validators=[
      DataRequired('이메일 필수 입력'),
      Email(message="이메일 형식으로 다시")
    ]
  )
  password = PasswordField(
    "비밀번호",
    validators=[
      DataRequired('비번 필수 입력')
    ]
  )
  submit = SubmitField('가입버튼')

class LoginForm(FlaskForm):
  username = StringField(
    "사용자명",
    validators=[
      DataRequired('사용자명 필수 입력'),
      Length(3,20,"3~30자 이내로 입력")
    ]
  )

  password = PasswordField(
    "비밀번호",
    validators=[
      DataRequired('비번 필수 입력')
    ]
  )
  submit = SubmitField('로그인')