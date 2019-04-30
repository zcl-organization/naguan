# -*- coding:utf-8 -*-

# from app import create_app
# flask_app = create_app('develop')
#
# from app.exts import celery

# import os
#
# from flask_celery import Celery
# from app import create_app


import os
from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()



