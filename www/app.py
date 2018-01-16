#!/usr/bin/env python3

from sqlalchemy import *

from www import APP
from www.models import DB
from www.views import *

from config import CURRENT_CONFIG

if __name__ == '__main__':
    DB.create_all()
    DB.session.commit()
    APP.run(use_reloader=False, debug=CURRENT_CONFIG.DEBUG)
