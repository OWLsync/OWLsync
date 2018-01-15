#!/usr/bin/env python3

# ADD DATA TO DB

from www import DB
from www.models import User
#from www.models import User, Post


DB.create_all()
try:
    user_data = User()
    user_data.user_first_name = "Jo"
    user_data.user_last_name = 'Some'
    DB.session.add(user_data)

    DB.session.commit()  # calls flush beforehand, but we need it after the commit
    DB.session.flush()  # updates the objects of the session
    print(user_data)  # Print object updated after the flush
except Exception as e:
    DB.session.rollback()
    print(e)

# post_data
if False:
    try:
        post_data = Post()
        post_data.body = "Hello World"
        post_data.user_id = user_data.id
        DB.session.add(post_data)

        DB.session.commit()  # calls flush beforehand, but we need it after the commit
        DB.session.flush()  # updates the objects of the session
        print(post_data)  # Print object updated after the flush
    except Exception as e:
        DB.session.rollback()
        print(e)
