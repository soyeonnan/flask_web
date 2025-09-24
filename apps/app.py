from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

from apps.config import config
import os

config_key = os.environ.get("FLASK_CONFIG_KEY")

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
  app = Flask(__name__)

  app.config.from_object(config[config_key])

  csrf.init_app(app)
  db.init_app(app)
  Migrate(app, db)
  login_manager.init_app(app)
  login_manager.login_view = 'auth.login'
  login_manager.login_message = '로그인 후 이용 가능'

  
  from apps.crud import views as crud_views
  from apps.study import views as study_views
  from apps.auth import views as auth_views
  from apps.detector import views as dt_views

  app.register_blueprint(crud_views.crud, url_prefix='/crud')
  app.register_blueprint(study_views.study, url_prefix="/study")
  app.register_blueprint(auth_views.auth, url_prefix="/auth")
  app.register_blueprint(dt_views.dt) # 기본 도메인으로 시작한다는 것임

  return app