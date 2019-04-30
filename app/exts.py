from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask import current_app
from celery import Celery
from config import BaseConfig

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db)


# celery = Celery()

celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL)
