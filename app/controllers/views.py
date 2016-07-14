from flask import render_template

from ..models import Channel
from . import controllers
from ..decorators import channel_permission_required


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
