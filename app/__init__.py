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
from app.models.user import current_user
from app.models.channel import Channel
from app.models.channel import ChannelPermission
from app.models.user import User


@app.context_processor
def current_user_processor():
    return dict(current_user=current_user())


@app.context_processor
def channel_processor():
    channels = Channel.query.all()
    permissions = [
        ChannelPermission.NORMAL,
        ChannelPermission.ADMIN,
    ]
    dic = {
        'channels': channels,
        'permissions': permissions,
    }
    return dict(**dic)


@app.context_processor
def user_processor():
    user_count = User.query.count()
    new_user = User.query.order_by(User.created_time.desc()).first()
    return dict(new_user=new_user,
                user_count=user_count)
