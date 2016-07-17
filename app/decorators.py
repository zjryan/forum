from flask import abort
from functools import wraps
from .models import current_user
from .models import Channel
from .models import Post


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            abort(405)
        return f(*args, **kwargs)
    return wrapped


def channel_permission_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        channel_id = kwargs.get('id')
        channel = Channel.channel_by_id(channel_id)
        user = current_user()
        if user is None:
            permission = 0x01
        else:
            permission = user.permissions()
        if permission & channel.permission == 0:
            abort(401)
        return f(*args, **kwargs)
    return wrapped


def post_permission_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        post_id = kwargs.get('id')
        post = Post.post_by_id(post_id)
        channel_id = post.channel_id
        channel = Channel.channel_by_id(channel_id)
        user = current_user()
        if user is None:
            permission = 0x01
        else:
            permission = user.permissions()
        if permission & channel.permission == 0:
            abort(401)
        return f(*args, **kwargs)
    return wrapped