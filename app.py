from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

from config import Configuration  # import our configuration data.

app = Flask(__name__)

app.config.from_object(Configuration)  # use values from our

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# ____________________POSTGRES CONNECTION

DB_url = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=app.config["POSTGRES_USER"],
    pw=app.config["POSTGRES_PW"],
    url=app.config["POSTGRES_URL"],
    db=app.config["POSTGRES_DB"])

app.config['SQLALCHEMY_DATABASE_URI'] = DB_url

# _________________________________________
engine = create_engine(DB_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
# ________________________________________

SECRET_KEY = app.config["SECRET_KEY"]
DOMAIN_SERVER = app.config["DOMAIN_SERVER"]


#  ____________________DB MODELS_________________________
class Person(Base):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    user = relationship("User", backref="person")

    def __init__(self):
        pass

    def __repr__(self):
        return '<Person: id={0.id!r}, name={0.name!r}>'.format(self)


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('person.id'))

    person = relationship(Person)

    def __init__(self):
        pass

    def __repr__(self):
        return '<User %r>' % self.username


# The above configuration establishes a collection of Address objects on User called Person.user
# It also establishes a .person attribute on User which will refer to the parent Person object.
# http://docs.sqlalchemy.org/en/latest/orm/backref.html


# ___ FORM ___ USER ___ START ___

class Userform(FlaskForm):
    name = StringField('name', validators=[DataRequired("name here.")])
    username = StringField('username', validators=[DataRequired("username here.")])
    email = StringField('email', validators=[DataRequired("email here")])
    user_join_date = DateField('user_join_date', format='%Y-%m-%d')
    submit = SubmitField("Submit")


# ___ FORM ___ USER ___ END ___


# ___ USER ___ REGISTER ___ START ___

@app.route('/userregister', methods=('GET', 'POST'))
def userregister():
    form = Userform()
    if form.validate_on_submit():
        try:
            db.create_all()

            person_data = Person()
            person_data.name = form.name.data  # ___ NAME

            db.session.add(person_data)
            db.session.commit()  # calls flush beforehand, but we need it after the commit.
            db.session.flush()  # updates the objects of the session.

            print("{0}".format(person_data.name))

            user_data = User()
            user_data.username = form.username.data  # ___ USERNAME
            user_data.email = form.email.data  # ___ EMAIL
            user_data.user_join_date = form.user_join_date.data  # ___ EMAIL

            db.session.add(user_data)
            db.session.commit()  # calls flush beforehand, but we need it after the commit.
            db.session.flush()  # updates the objects of the session.

            print("{0}  {1}  {2}".format(
                user_data.username,
                user_data.email,
                user_data.user_join_date))

        except Exception as e:
            db.session.rollback()
            print(e)
    return render_template('userregister.html', form=form)


# ___ USER ___ REGISTER ___ ENDS ___


# VIEWS
@app.route("/")
@app.route("/index")
def index():
    try:
        users = db.session.query(User).all()
        return render_template("index.html", users=users)
    except Exception as e:
        return str(e)


@app.route('/posts')
def view_posts():
    users = db.session.query(User).all()
    return render_template("posts.html", users=users), 200


if __name__ == '__main__':
    app.run(use_reloader=False, debug=True)
