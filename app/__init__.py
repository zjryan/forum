# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand


app = Flask(__name__)
app.secret_key = 'jgn3-kigf-4bgk-0ndv'
app.config.from_object('config')
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


from app import views
from app import filters
from app import context_processers



