from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from flask import Flask

from config import CURRENT_CONFIG

APP = Flask(__name__)

APP.config.from_object(CURRENT_CONFIG)

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if CURRENT_CONFIG.DEBUG:
    APP.config['SQLALCHEMY_ECHO'] = True

APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=APP.config["POSTGRES_USER"],
    pw=APP.config["POSTGRES_PW"],
    url=APP.config["POSTGRES_URL"],
    db=APP.config["POSTGRES_DB"])
