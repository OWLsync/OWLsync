#!/usr/bin/env python3

from flask import render_template
from flask_wtf import FlaskForm
from sqlalchemy import *
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#session_factory = sessionmaker(bind=ENGINE)
#Session = scoped_session(session_factory)

from www import APP, DB
from www.models import User

SECRET_KEY = APP.config["SECRET_KEY"]
DOMAIN_SERVER = APP.config["DOMAIN_SERVER"]


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
    DB.create_all()
    APP.run(use_reloader=False, debug=True)
