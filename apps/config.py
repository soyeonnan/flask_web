import secrets

# 전체 환경 공통 설정들...
class BaseConfig:
  SECRET_KEY = secrets.token_urlsafe(32)
  WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(32)

# 로컬환경에서 적용할 환경설정들..
class LocalConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True

# 배포환경에서 적용할 환경설정들..
class DeployConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='배포 후 사용할 DB주소'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=False

config = {
  "local" : LocalConfig,
  "deploy" : DeployConfig
}