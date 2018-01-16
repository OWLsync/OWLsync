from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from www import APP

DB = SQLAlchemy(APP)


class Person(DB.Model):
    __tablename__ = 'person'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(250), nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return '<Person: id={0.id!r}, name={0.name!r}>'.format(self)


class User(DB.Model):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(200), unique=True, nullable=True)
    email = DB.Column(DB.String(200), unique=False, nullable=True)
    user_join_date = DB.Column(DB.DateTime, nullable=False, default=datetime.now().date())

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<Stats: id={0.id!r}, user_name={0.user_name!r}>'.format(self)


class Article(DB.Model):
    __tablename__ = 'article'
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(140))
    body = DB.Column(DB.String(140))
    timestamp = DB.Column(DB.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Article: id={0.id!r}, title={0.title!r}>'.format(self)

    # def _get_articles(self):
    #     return DB.object_session(self).query(Article).with_parent(self).all()
    #     articles = property(_get_article)
