# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.secret_key = 'jgn3-kigf-4bgk-0ndv'
    db.init_app(app)
    db.app = app

    from .accounts import accounts as accounts_blueprint
    from .controllers import controllers as controllers_blueprint
    from .api import api as api_blueprint
    app.register_blueprint(accounts_blueprint)
    app.register_blueprint(controllers_blueprint)
    app.register_blueprint(api_blueprint)

    return app



