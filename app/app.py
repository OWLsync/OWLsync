#!/usr/bin/env python3

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from config import Configuration  # import our configuration data.

APP = Flask(__name__)

APP.config.from_object(Configuration)  # use values from our

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_ECHO'] = True

DB = SQLAlchemy(APP)

# ____________________POSTGRES CONNECTION

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=APP.config["POSTGRES_USER"],
    pw=APP.config["POSTGRES_PW"], url=APP.config["POSTGRES_URL"], db=APP.config["POSTGRES_DB"])

APP.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

# _________________________________________
ENGINE = create_engine(DB_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

BASE = declarative_base()
BASE.query = db_session.query_property()

session_factory = sessionmaker(bind=ENGINE)
Session = scoped_session(session_factory)
# ________________________________________

SECRET_KEY = APP.config["SECRET_KEY"]
DOMAIN_SERVER = APP.config["DOMAIN_SERVER"]


# DB MODELS
class User(BASE):
    __tablename__ = 'user'
    id = DB.Column(DB.Integer, primary_key=True)
    user_first_name = DB.Column(DB.String(35), unique=False, nullable=False)
    user_last_name = DB.Column(DB.String(35), unique=False, nullable=False)
    posts = DB.Column(DB.String(2000), unique=False, nullable=False)


# xu = User.query.order_by('-id').first()
# print(xu)


class Userform(FlaskForm):
    user_first_name = StringField('user_first_name', validators=[DataRequired("Please enter your first name.")])
    user_last_name = StringField('user_last_name', validators=[DataRequired("Please enter your last name.")])
    posts = StringField('name', validators=[DataRequired("Please enter your post.")])
    submit = SubmitField("Submit")


@APP.route('/userregister', methods=('GET', 'POST'))
def userregister():
    form = Userform()
    if form.validate_on_submit():
        try:
            DB.create_all()
            user_data = User()
            user_data.user_first_name = form.user_first_name.data
            user_data.user_last_name = form.user_last_name.data
            user_data.posts = form.posts.data
            DB.session.add(user_data)
            DB.session.commit()  # calls flush beforehand, but we need it after the commit
            print("{0}  {1}  {2}".format(user_data.user_first_name, user_data.user_last_name, user_data.posts))
            DB.session.flush()  # updates the objects of the session
        except Exception as e:
            DB.session.rollback()
            print(e)
    return render_template('userregister.html', form=form)


# VIEWS
@APP.route("/")
@APP.route("/index")
def index():
    try:
        Users = DB.session.query(User).all()
        return render_template("index.html", Users=Users)
    except Exception as e:
        return str(e)

@APP.route('/posts')
def view_posts():
    Users = DB.session.query(User).all()
    return render_template("posts.html", Users=Users), 200


if __name__ == '__main__':
    APP.run(use_reloader=False, debug=True)
