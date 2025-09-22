from flask import Blueprint, render_template

from apps.crud.forms import UserForm
from apps.crud.models import User
from apps.app import db

crud = Blueprint(
  "crud", # 블루 프린트의 이름 지정
  __name__, # 블루 프린트가 정의 된 모듈명
  template_folder="templates", # 해당 블루 프린트와 관련 된 템플릿 파일이 있는 폴더
  static_folder="static" # 해당 블루 프린트와 관련 된 정적 파일이 있는 폴더
)

@crud.route("/")
def index():
  return render_template("crud/index.html")

@crud.route("/users/new", methods = ['GET','POST'])
def create_user():
  form = UserForm() 

  return render_template('crud/create.html', form=form)