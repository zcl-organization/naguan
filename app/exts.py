# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery, platforms
from config import BaseConfig

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db)


# celery = Celery()
platforms.C_FORCE_ROOT =True
celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL)
