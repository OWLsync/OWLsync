from flask import Flask, render_template
from datetime import datetime
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

from config import Configuration  # import our configuration data.

app = Flask(__name__)
app.config.from_object(Configuration)  # use values from our
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SECRET_KEY = app.config["SECRET_KEY"]
DOMAIN_SERVER = app.config["DOMAIN_SERVER"]
POSTGRES_URL = app.config["POSTGRES_URL"]
POSTGRES_DB = app.config["POSTGRES_DB"]
POSTGRES_USER = app.config["POSTGRES_USER"]
POSTGRES_PW = app.config["POSTGRES_PW"]

# POSTGRES CONNECTION
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
    pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)


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

    # Define the slug field from Posts.
    def slug(self):
        return quote_plus(self.body)


# ADD DATA TO DB
# user_data
try:
    db.create_all()
    user_data = User()
    user_data.user_first_name = 'Peter'
    user_data.user_last_name = 'Some'
    db.session.add(user_data)

    db.session.commit()  # calls flush beforehand, but we need it after the commit
    db.session.flush()  # updates the objects of the session
except Exception:
    db.session.rollback()

try:
    post_data = Post()
    post_data.body = "Hello World"
    post_data.user_id = user_data.id
    db.session.add(post_data)

    db.session.commit()  # calls flush beforehand, but we need it after the commit
    db.session.flush()  # updates the objects of the session
except Exception:
    db.session.rollback()

print(user_data, post_data)  # id field of the User object updated after the flush


# VIEWS
@app.route("/")
@app.route("/index")
def index():
    try:
        return render_template("index.html"), 200
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
    app.run(use_reloader=False)
