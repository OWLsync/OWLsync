# ADD DATA TO DB
# user_data
try:
    db.create_all()
    user_data = User()
    user_data.user_first_name = "Jo"
    user_data.user_last_name = 'Some'
    db.session.add(user_data)

    db.session.commit()  # calls flush beforehand, but we need it after the commit
    db.session.flush()  # updates the objects of the session
except Exception as e:
    db.session.rollback()
    print(e)

try:
    post_data = Post()
    post_data.body = "Hello World"
    post_data.user_id = user_data.id
    db.session.add(post_data)

    db.session.commit()  # calls flush beforehand, but we need it after the commit
    db.session.flush()  # updates the objects of the session
except Exception as e:
    db.session.rollback()
    print(e)

print(user_data, post_data)  # Print object updated after the flush
