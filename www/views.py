from flask import render_template

from www import APP, DB
from www.models import User
from www.forms import Userform

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

