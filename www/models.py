from datetime import datetime

from www import BASE, DB


class User(BASE):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True)
    user_name = DB.Column(DB.String(200), unique=False, nullable=True)
    email = DB.Column(DB.String(200), unique=False, nullable=True)

    posts = DB.relationship('Post', backref='author', lazy='dynamic')

    # # http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#building-query-enabled-properties
    #
    #     def _get_articles(self):
    #         return DB.object_session(self).query(Article).with_parent(self).all()
    #         articles = property(_get_article)

    def __repr__(self):
        return '<Stats: id={0.id!r}, user_name={0.user_name!r}>'.format(self)


class Article(BASE):
    __tablename__ = 'article'
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(140))
    body = DB.Column(DB.String(140))
    timestamp = DB.Column(DB.DateTime, index=True, default=datetime.utcnow)

    author = DB.Column(DB.Integer, DB.ForeignKey("user.id"))

# The above configuration establishes a collection of Article objects on User called User.article.
# It also establishes a .user attribute on Article which will refer to the parent User object.
