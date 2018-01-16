from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField

from wtforms.validators import DataRequired

class Userform(FlaskForm):
    name = StringField('name', validators=[DataRequired("name here.")])
    username = StringField('username', validators=[DataRequired("username here.")])
    email = StringField('email', validators=[DataRequired("email here")])
    user_join_date = DateField('user_join_date', format='%Y-%m-%d')
    submit = SubmitField("Submit")


class Articleform(FlaskForm):
    title = StringField('body', validators=[DataRequired("title here")])
    body = StringField('body', validators=[DataRequired("body here")])
    timestamp = StringField('user_last_name', validators=[DataRequired("timestamp here")])
    submit = SubmitField("Submit")
