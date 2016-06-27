# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

import time
import shutil
import os

from ..utilities import log


app = Flask(__name__)
app.secret_key = 'ert4-bgs6-3rew-hj9x'
db_path = 'app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


class Model(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = (u'{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return u'\n<{0}:\n  {1}\n'.format(class_name, '\n    '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def backup_db():
    backup_path = 'migration/{}_{}'.format(time.time(), 'models.db')
    shutil.copyfile(db_path, backup_path)


def rebuild_db():
    if os.path.exists(db_path):
        backup_db()
    db.drop_all()
    db.create_all()
    log('rebuilt database successfully')

