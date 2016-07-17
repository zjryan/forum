# encoding: utf-8

from flask import render_template
from flask import request
from flask import url_for

from .models.channel import Channel
from .models.channel import ChannelPermission
from .models.comment import Comment
from .models.user import User
from .models.user import current_user

from app import app


def url_back(route='index'):
    return request.args.get('next') \
                        or request.referrer \
                        or url_for(route)


@app.route('/')
def index():
    posts = []
    user = current_user()
    if user is None:
        permissions = 0x01
    else:
        permissions = user.permissions()

    channels = Channel.query.all()
    for channel in channels:
        if permissions & channel.permission:
            posts += channel.posts
    return render_template('index.html', posts=posts)