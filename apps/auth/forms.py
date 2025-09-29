from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
  username = StringField(
    "사용자명",
    validators=[
      DataRequired('사용자명은 필수입니다.'),
      Length(3, 20, "3~20글자까지 가능합니다.")
    ]
  )
  email = StringField(
    "메일주소",
    validators=[
      DataRequired('메일 주소는 필수입력'),
      Email('메일 형식으로 입력하세요')
    ]
  )
  password = PasswordField(
    "비밀번호",
    validators=[
      DataRequired('비밀번호는 필수')
    ]
  )
  submit = SubmitField('가입')

class LoginForm(FlaskForm):
  username = StringField(
    "사용자명",
    validators=[
      DataRequired('사용자명은 필수입니다.'),
      Length(3, 20, "3~20글자까지 가능합니다.")
    ]
  )
  password = PasswordField(
    "비밀번호",
    validators=[
      DataRequired('비밀번호는 필수')
    ]
  )
  submit = SubmitField('로그인')