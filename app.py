from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from config import Configuration  # import our configuration data.

app = Flask(__name__)

app.config.from_object(Configuration)  # use values from our

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# ____________________POSTGRES CONNECTION

DB_url = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=app.config["POSTGRES_USER"],
    pw=app.config["POSTGRES_PW"], url=app.config["POSTGRES_URL"], db=app.config["POSTGRES_DB"])

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


# DB MODELS
class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(35), unique=False, nullable=False)
    user_last_name = db.Column(db.String(35), unique=False, nullable=False)
    posts = db.Column(db.String(200), unique=False, nullable=False)


# xu = User.query.order_by('-id').first()
# print(xu)


class Userform(FlaskForm):
    user_first_name = StringField('user_first_name', validators=[DataRequired("Please enter your first name.")])
    user_last_name = StringField('user_last_name', validators=[DataRequired("Please enter your last name.")])
    posts = StringField('name', validators=[DataRequired("Please enter your post.")])
    submit = SubmitField("Submit")


@app.route('/userregister', methods=('GET', 'POST'))
def userregister():
    form = Userform()
    if form.validate_on_submit():
        try:
            db.create_all()
            user_data = User()
            user_data.user_first_name = form.user_first_name.data
            user_data.user_last_name = form.user_last_name.data
            user_data.posts = form.posts.data
            db.session.add(user_data)
            db.session.commit()  # calls flush beforehand, but we need it after the commit
            db.session.flush()  # updates the objects of the session
        except Exception as e:
            db.session.rollback()
            print(e)
    return render_template('userregister.html', form=form)




# VIEWS
@app.route("/")
@app.route("/index")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)


@app.route('/posts')
def view_posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts), 200


@app.route('/post/<post_id>/<slug>')
def view_post(post_id, slug):
    post = Post.query.get(post_id)
    return render_template("post.html", post=post), 200


if __name__ == '__main__':
    app.run(use_reloader=False, debug=True)
