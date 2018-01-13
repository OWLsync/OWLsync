from app import db
from datetime import datetime


# DB MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(200), unique=False, nullable=True)
    user_last_name = db.Column(db.String(200), unique=False, nullable=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # Define relation to the Post


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
