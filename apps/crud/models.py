# 엔티티
from apps.app import db
from werkzeug.security import generate_password_hash # 패싱 해주는 거(비번 암호화)

from datetime import datetime

class User(db.Model):
  # db에 생성되는 테이블 명 지정
  __tablename__ = "users"

  # 컬럼들...
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), index=True)
  email = db.Column(db.String(255), unique=True, index=True)
  password_hash = db.Column(db.String(255))
  create_at = db.Column(db.DateTime, default=datetime.now)
  update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) # onupdate -> 수정 된 날짜로 변경 작동

  @property # 예외 발생 (getter) -> 외부에서 못 읽게 하려고
  def password(self):
    raise AttributeError("읽을 수 없음") # 비번 못 보게 강제로 예외 발생
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password) # 암호화 처리 후 변수에 넣어라