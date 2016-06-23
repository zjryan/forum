# encoding: utf-8

from flask import redirect
from flask import render_template
from flask import url_for

from .models.channel import Channel
from app import app


@app.route('/')
def index():
    return redirect(url_for('channels_view'))


@app.route('/channels')
def channels_view():
    channels = Channel.query.all()
    return render_template('channels.html', channels=channels)