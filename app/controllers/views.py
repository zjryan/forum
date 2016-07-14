from flask import render_template

from ..models import Channel
from . import controllers


@controllers.route('/channel/<int:id>')
def channel_view(id):
    channel = Channel.channel_by_id(id)
    return render_template('channel.html', channel=channel)
