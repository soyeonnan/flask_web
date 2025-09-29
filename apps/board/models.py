from datetime import datetime

from apps.app import db

class Board(db.Model):
  __tablename__ = 'board'
  id = db.Column(db.Integer, primary_key=True)
  subject = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  user = db.relationship('User', backref=db.backref('boards'))

class Reply(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  user = db.relationship('User', backref=db.backref('user_replies'))
  board_id = db.Column(db.Integer, db.ForeignKey('board.id', ondelete='CASCADE'))
  board = db.relationship('Board', backref=db.backref('reply_list'))
