# encoding: utf-8

from flask import redirect
from flask import render_template
from flask import url_for
from flask import request

from .models.channel import Channel
from .models.post import Post
from .models.user import User
from .utilities import log
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


@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    u = User(request.form)
    user = User.query.filter_by(username=u.username).first()
    if user.login_valid(u):
        log(user.username, '登录成功')
        return redirect(url_for('channels'))
    else:
        log(user.username, '登录失败')
        return redirect(url_for('login_view'))


@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    if User.register_valid(request.form):
        user = User(request.form)
        user.save()
        log(user.username, '用户注册成功')
        return redirect(url_for('login_view'))
    else:
        log('用户注册失败')
        return redirect(url_for('register_view'))

