from flask import render_template
from flask import request
from flask import url_for

from ..models import Channel
from ..models import Post
from ..models import current_user
from . import controllers
from ..decorators import channel_permission_required
from ..decorators import post_permission_required


def url_back(route='controllers.index'):
    return request.args.get('next') \
                        or request.referrer \
                        or url_for(route)


@controllers.route('/channel/<int:id>')
@channel_permission_required
def channel_view(id):
    channel = Channel.channel_by_id(id)
    posts = channel.posts
    d = dict(
        posts=posts,
        channel=channel
    )
    return render_template('channel.html', **d)


@controllers.route('/post/<int:id>')
@post_permission_required
def post_view(id):
    post = Post.post_by_id(id)
    comments = post.comments
    d = dict(
        post=post,
        comments=comments
    )
    return render_template('post.html', **d)


@controllers.route('/')
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