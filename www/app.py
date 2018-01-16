#!/usr/bin/env python3

from www import APP, DB
from www.models import User
from www.views import *

from config import CURRENT_CONFIG

if __name__ == '__main__':
    DB.create_all()
    APP.run(use_reloader=False, debug=CURRENT_CONFIG.DEBUG)
