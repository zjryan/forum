# encoding: utf-8

from flask import Flask


app = Flask(__name__)
app.secret_key = 'jgn3-kigf-4bgk-0ndv'


from app import views
from .models.user import current_user
from .models.channel import Channel
from .models.user import User


@app.context_processor
def current_user_processor():
    return dict(current_user=current_user())


@app.context_processor
def channel_processor():
    channels = Channel.query.all()
    return dict(channels=channels)


@app.context_processor
def user_processor():
    user_count = User.query.count()
    new_user = User.query.order_by(User.created_time.desc()).first()
    return dict(new_user=new_user,
                user_count=user_count)
