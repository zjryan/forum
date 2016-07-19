# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from app import init_app
from app import db

app = init_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

