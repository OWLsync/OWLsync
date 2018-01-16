#!/usr/bin/env python3
from flask_wtf.csrf import CSRFProtect
from www import APP
from www.models import DB

from www.views import *

from config import CURRENT_CONFIG

csrf = CSRFProtect(APP)

if __name__ == '__main__':
    # DB.create_all()
    # DB.session.commit()
    APP.run(use_reloader=False, debug=CURRENT_CONFIG.DEBUG)
    csrf.init_app(APP)
