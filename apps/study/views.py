from flask import Blueprint, render_template, redirect, url_for
from apps.study.forms import WriteForm

from apps.app import db
from apps.study.models import Study

study = Blueprint(
  "study",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@study.route("/")
def index():
  study = Study.query.order_by( Study.id.desc() ).all()

  return render_template('study/index.html', study=study)

@study.route("/write", methods=['GET', 'POST'])
def write():
  form = WriteForm()

  if form.validate_on_submit():
    study = Study(
      subject = form.subject.data,
      writer = form.writer.data,
      content = form.content.data
    )

    db.session.add(study)
    db.session.commit()

    return redirect( url_for('study.index') )

  return render_template('study/write.html', form=form)

@study.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  data = Study.query.get(id)
  form = WriteForm(obj = data)

  if form.validate_on_submit():
    data.subject = form.subject.data
    data.writer = form.writer.data
    data.content = form.content.data

    db.session.add(data)
    db.session.commit()

    return redirect(url_for('study.index'))
  
  return render_template("study/edit.html", data=data, form=form)

@study.route('/delete/<int:id>')
def delete_data(id):
  data = Study.query.get(id)
  db.session.delete(data)
  db.session.commit()

  return redirect( url_for('study.index') )