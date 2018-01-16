from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import *

from www import APP

DB = SQLAlchemy(APP)

class Person(DB.Model):
    __tablename__ = 'person'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(250), nullable=False)
    user = DB.relationship("User", backref="person")
    #def __init__(self):
    #    pass
    def __repr__(self):
        return '<Person: id={0.id!r}, name={0.name!r}>'.format(self)

class User(DB.Model):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(200), unique=False, nullable=True)
    email = DB.Column(DB.String(200), unique=False, nullable=True)
    user_join_date = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('person.id'))
    #person = DB.relationship(Person)
    articles = DB.relationship('Article', backref='author', lazy='dynamic')
    #def _get_articles(self):
    #   return DB.object_session(self).query(Article).with_parent(self).all()
    #   #articles = property(_get_article)
    #def __init__(self):
    #    pass
    def __repr__(self):
        return '<Stats: id={0.id!r}, user_name={0.user_name!r}>'.format(self)

class Article(DB.Model):
    __tablename__ = 'article'
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(140))
    body = DB.Column(DB.String(140))
    timestamp = DB.Column(DB.DateTime, index=True, default=datetime.utcnow)
    written_by_author = DB.Column(DB.Integer, DB.ForeignKey("user.id"))