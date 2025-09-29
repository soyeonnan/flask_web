from flask import Flask, render_template
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
login_manager.login_view = 'auth.login'
login_manager.login_message = '로그인 후 이용 가능합니다.'

def create_app():
  app = Flask(__name__)

  app.config.from_object(config[config_key])

  csrf.init_app(app)
  db.init_app(app)
  Migrate(app, db)
  login_manager.init_app(app)

  from apps.crud import views as crud_views
  from apps.study import views as study_views
  from apps.auth import views as auth_views
  from apps.detector import views as dt_views
  from apps.board import views as board_views
  from apps.board import reply_views

  app.register_blueprint(crud_views.crud, url_prefix='/crud')
  app.register_blueprint(study_views.study, url_prefix="/study")
  app.register_blueprint(auth_views.auth, url_prefix='/auth')
  app.register_blueprint(dt_views.dt)
  app.register_blueprint(board_views.bp, url_prefix='/board')
  app.register_blueprint(reply_views.reply, url_prefix='/reply')

  app.register_error_handler(404, page_not_found)
  app.register_error_handler(500, internal_server_error)

  # 오류 구분 없이 모든 오류발생 시 처리하도록 할거면
  # app.register_error_handler(Exception, 실행할함수)

  return app

def page_not_found(e):
  return render_template('404.html'), 404

def internal_server_error(e):
  return render_template('500.html'), 500