#!/usr/bin/env python3

# ADD DATA TO DB

from www import APP
from www.models import User, Article, DB

# DB.create_all()
# DB.session.commit()
#
# if False:
#     try:
#         user_data = User()
#         user_data.user_first_name = "Jo"
#         user_data.user_last_name = 'Some'
#         DB.session.add(user_data)
#
#         DB.session.commit()
#         DB.session.flush()
#         print(user_data)
#     except Exception as e:
#         DB.session.rollback()
#         print("Problem: ", e)
#
#     try:
#         article_data = Article()
#         article_data.title = "Hello"
#         article_data.body = "Hello World"
#         article_data.written_by_author = user_data.id
#         DB.session.add(article_data)
#
#         DB.session.commit()
#         DB.session.flush()
#         print(article_data)
#     except Exception as e:
#         DB.session.rollback()
#         print("Problem: ", e)
