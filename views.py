from app import app
from flask import request, render_template

domain = "http://127.0.0.1:5000"


@app.route("/")
@app.route("/index")
def index():
    try:
        return render_template("index.html", domain=domain), 200
    except Exception as e:
        return str(e)


@app.route("/about")
def about():
    try:
        return render_template("about.html"), 200
    except Exception as e:
        return str(e)


@app.route("/contact")
def contact():
    try:
        return render_template("contact.html"), 200
    except Exception as e:
        return str(e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logic for handling login
        pass
    else:
        # Display login form
        pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
