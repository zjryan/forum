# encoding: utf-8

from flask import redirect
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from flask import abort

from .models.channel import Channel
from .models.post import Post
from .models.user import User
from .models.user import current_user
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
    posts = channel.posts
    posts.sort(key=lambda p: p.created_time, reverse=True)
    return render_template('channel.html',
                           channel=channel,
                           posts=posts)


@app.route('/channel/<int:channel_id>/add_post', methods=['POST'])
def post_add(channel_id):
    post = Post(request.form)
    user = current_user()
    if post.post_valid():
        post.set_channel(channel_id)
        post.set_author(user.id)
        post.save()
        log('帖子', post.id, '标题:' ,post.title , '发送成功 作者:', post.author.username)
    else:
        log('帖子发送失败')
    return redirect(url_for('channel_view', id=channel_id))


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
    username = request.form.get('username', '')
    user = User.query.filter_by(username=username).first()
    if user.login_valid(request.form):
        log(user.username, '登录成功')
        session['user_key'] = user.id
        return redirect(url_for('channels'))
    else:
        log(user.username, '登录失败')
        return redirect(url_for('login_view'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('channels'))


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


@app.route('/profile/<username>')
def profile(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    return render_template('profile.html', user=u)

