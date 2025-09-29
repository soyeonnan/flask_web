from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user

from apps.auth.forms import SignUpForm, LoginForm
from apps.app import db
from apps.crud.models import User

auth = Blueprint(
  "auth",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@auth.route('/')
def index():
  return render_template('auth/index.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUpForm()

  if form.validate_on_submit():
    user = User(
      username = form.username.data,
      email = form.email.data,
      password = form.password.data
    )

    if user.is_duplicate_email():
      flash('해당 이메일은 이미 등록되어있습니다.')
      return render_template('auth/signup.html', form=form)
    
    db.session.add(user)
    db.session.commit()

    return redirect( url_for('detector.index') )

  return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    # DB에서 로그인하려고 하는 사람의 아이디를 이용해서 레코드를 꺼내와야 함
    user = User.query.filter_by(username=form.username.data).first()

    # DB에서 꺼내온 정보의 비번과 로그인할때 입력한 비번이 일치하는지 체크
    if user is not None and user.verify_password(form.password.data):
      login_user(user)

      next_ = request.args.get('next')
      if next_ is None or not next_.startswith('/'):
        next_ = url_for('detector.index')

      return redirect( next_ )

    flash('아이디 비번이 잘못됨')
  return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
  logout_user()
  return redirect( url_for('detector.index') )