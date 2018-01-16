from flask import render_template

from www import APP
from www.models import DB, User, Person
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
            user_data.username = form.username.data
            user_data.email = form.email.data
            user_data.user_join_date = form.user_join_date.data

            DB.session.add(user_data)
            DB.session.commit()
            DB.session.flush()
            print("{0}  {1}  {2}".format(
                user_data.username,
                user_data.email,
                user_data.user_join_date))

            person_data = Person()
            person_data.name = form.name.data
            person_data.user = user_data

            DB.session.add(person_data)
            DB.session.commit()
            DB.session.flush()
            print("{0}".format(person_data.name))

        except Exception as e:
            DB.session.rollback()
            print(e)
    return render_template('userregister.html', form=form)
