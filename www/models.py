from datetime import datetime

from www import BASE, DB

class User(DB.Model):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True)
    user_first_name = DB.Column(DB.String(200), unique=False, nullable=True)
    user_last_name = DB.Column(DB.String(200), unique=False, nullable=True)
    posts = DB.relationship('Post', backref='author', lazy='dynamic')

class Post(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    body = DB.Column(DB.String(140))
    timestamp = DB.Column(DB.DateTime, index=True, default=datetime.utcnow)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"))

