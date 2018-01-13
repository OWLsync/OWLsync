from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ------------------ Configuration Handling START  ///
app.config.from_object('config.Configuration')  # config.py

#  ----   POSTGRES SQLALCHEMY CONFIG START ///

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # allows you to disable the modification tracking system
db = SQLAlchemy(app)

#  ----   POSTGRES SQLALCHEMY CONFIG END ///




engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():

    Base.metadata.create_all(bind=engine)



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




from views import *



if __name__ == "__main__":
    init_db()
    app.run()
