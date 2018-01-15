from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired

class Userform(FlaskForm):
    user_first_name = StringField('user_first_name', validators=[DataRequired("Please enter your first name.")])
    user_last_name = StringField('user_last_name', validators=[DataRequired("Please enter your last name.")])
    posts = StringField('name', validators=[DataRequired("Please enter your post.")])
    submit = SubmitField("Submit")

