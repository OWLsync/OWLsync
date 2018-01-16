from flask import render_template, request
from datetime import datetime

from www import APP
from www.models import DB, User, Person
from www.forms import Userform

DB.create_all()
DB.session.commit()


@APP.route("/")
@APP.route("/index")
def index():
    try:
        users = DB.session.query(User).all()
        return render_template("index.html", users=users)
    except Exception as e:
        return str(e)


@APP.route('/posts')
def view_posts():
    Users = DB.session.query(User).all()
    return render_template("posts.html", Users=Users), 200


@APP.route('/userregister', methods=('GET', 'POST'))
def userregister():
    form = Userform(request.form)

    if request.method == 'POST' and form.validate():

        try:

            person_data = Person(name=form.name.data)
            DB.session.add(person_data)
            DB.session.commit()
            DB.session.flush()

            print("{0}".format(person_data.name))

        except Exception as e:
            DB.session.rollback()
            print(e)

        else:

            try:
                user_data = User(
                    username=form.username.data,
                    email=form.email.data)
                DB.session.add(user_data)
                DB.session.commit()
                DB.session.flush()

                print("{0}  {1}  {2}".format(
                    user_data.username,
                    user_data.email,
                    user_data.user_join_date))
            except Exception as e:
                DB.session.rollback()
                print(e)

    return render_template('userregister.html', form=form)
