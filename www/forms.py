from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired


class Userform(FlaskForm):
    user_name = StringField('user_first_name', validators=[DataRequired("user_name here")])
    email = StringField('user_last_name', validators=[DataRequired("email here")])
    submit = SubmitField("Submit")


class Articleform(FlaskForm):
    title = StringField('body', validators=[DataRequired("title here")])
    body = StringField('body', validators=[DataRequired("body here")])
    timestamp = StringField('user_last_name', validators=[DataRequired("timestamp here")])
    submit = SubmitField("Submit")
