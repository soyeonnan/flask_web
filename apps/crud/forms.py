from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
  username = StringField(
    "사용자명",
    validators=[
      DataRequired(message="사용자명은 필수"), # 유효성 검사에 실패하면 처리 할 메세지
      Length(max=30, message="사용자명은 30글자 이내로 입력바람") # Length -> 글자 수 
    ]
  )

  email = StringField(
    "이메일",
    validators=[
      DataRequired(message="이메일은 필수 입력"), # DataRequired -> 필수 입력
      Email(message="이메일 형식으로 입력 바람")
    ]
  )

  password = PasswordField(
    "비밀번호",
    validators=[
      DataRequired(message="비번은 필수") 
    ]
  )

  submit = SubmitField("회원가입")