from flask import render_template

from . import controllers


@controllers.route('/channel')
def channel_view():
    pass
