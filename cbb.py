#!/usr/bin/env python
import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
from injector import Module, Injector, singleton
from sqlalchemy.ext.declarative import declarative_base

from db import db
from routes.config import blueprint as config_blueprint


il = logging.getLogger('injector')
il.addHandler(logging.StreamHandler())
il.level = logging.DEBUG

# We use standard SQLAlchemy models rather than the Flask-SQLAlchemy magic, as
# it requires a global Flask app object and SQLAlchemy db object.
Base = declarative_base()


def main():
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'app.db')

    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'b3D$EJAQ4g91U8UPqwZ4yaaSoAsH!V')
    app.register_blueprint(config_blueprint, url_prefix='/config')
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///{0}'.format(db_path),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    app.debug = os.getenv('DEBUGGING', 'N') == 'Y'

    injector = Injector([AppModule(app)])
    FlaskInjector(app=app, injector=injector)

    app.run()


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    """Configure the application."""
    def configure(self, binder):
        # We configure the DB here, explicitly, as Flask-SQLAlchemy requires
        # the DB to be configured before request handlers are called.
        with self.app.app_context():
            db.init_app(self.app)
            Base.metadata.create_all(db.engine)
        binder.bind(SQLAlchemy, to=db, scope=singleton)


if __name__ == '__main__':
    main()
