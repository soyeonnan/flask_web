from datetime import datetime
from apps.app import db

class Study(db.Model):
  __tablename__ = 'study'
  id = db.Column(db.Integer, primary_key=True)
  subject = db.Column(db.String(255), nullable=True)
  content = db.Column(db.Text(), nullable=True)
  writer = db.Column(db.String(100), nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.now)
  
  def __str__(self):
    return f"id={self.id} subject={self.subject} content={self.content} writer={self.writer} created_at={self.created_at}"