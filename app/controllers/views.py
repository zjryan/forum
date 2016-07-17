from flask import render_template

from ..models import Channel
from ..models import Post
from . import controllers
from ..decorators import channel_permission_required
from ..decorators import post_permission_required


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
