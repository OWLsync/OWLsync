from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

APP = Flask(__name__)
APP.config.from_object(Configuration)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_ECHO'] = True

DB = SQLAlchemy(APP)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=APP.config["POSTGRES_USER"],
                                                                pw=APP.config["POSTGRES_PW"],
                                                                url=APP.config["POSTGRES_URL"],
                                                                db=APP.config["POSTGRES_DB"])
APP.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

ENGINE = create_engine(DB_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

BASE = declarative_base()
BASE.query = db_session.query_property()
