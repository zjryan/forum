# encoding: utf-8

from flask import redirect
from flask import render_template
from flask import url_for

from .models.channel import Channel
from .models.post import Post
from app import app


@app.route('/')
def index():
    return redirect(url_for('channels'))


@app.route('/channel/list')
def channels():
    channels = Channel.query.all()
    return render_template('channels.html',
                           channels=channels)


@app.route('/channel/<int:id>')
def channel_view(id):
    channel = Channel.query.get(id)
    return render_template('channel.html',
                           channel=channel)


@app.route('/post/list')
def posts():
    posts = Post.query.all()
    return render_template('posts.html',
                           posts=posts)


@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get(id)
    return render_template('post.html',
                           post=post)
