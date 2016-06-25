# encoding: utf-8

from flask import redirect
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from flask import abort
from flask import flash

from .models.channel import Channel
from .models.post import Post
from .models.user import User
from .models.comment import Comment
from .models.user import current_user
from .utilities import log
from app import app


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html',
                           posts=posts)


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
        flash('帖子发送成功')
    else:
        log('帖子发送失败')
        flash('帖子发送失败')
    return redirect(url_for('channel_view',
                            id=channel_id))


@app.route('/post/list')
def posts():
    posts = Post.query.all()
    return render_template('posts.html',
                           posts=posts)


@app.route('/post/<int:id>', methods=['GET'])
def post_view(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    comments = post.comments
    comments.sort(key=lambda c: c.created_time, reverse=True)
    return render_template('post.html',
                           post=post,
                           comments=comments)


@app.route('/post/<int:post_id>/add_comment', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get(post_id)
    if post is None:
        abort(404)
    comment = Comment(request.form)
    user = current_user()
    if comment.comment_valid() and user is not None:
        comment.set_author(user.id)
        comment.set_post(post_id)
        comment.save()
        log('回复成功 作者:', comment.author.username)
        flash('回复成功')
    else:
        log('回复失败')
        flash('回复失败')
    return redirect(url_for('post_view', id=post_id))


@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    user = User.query.filter_by(username=username).first()
    if user is not None and user.login_valid(request.form):
        log(user.username, '登录成功')
        flash('用户登录成功')
        session['user_key'] = user.id
        return redirect(url_for('index'))
    else:
        log('用户登录失败')
        flash('用户登录失败')
        return redirect(url_for('login_view'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    if User.register_valid(request.form):
        user = User(request.form)
        user.save()
        log(user.username, '用户注册成功')
        flash('用户注册成功')
        return redirect(url_for('login_view'))
    else:
        log('用户注册失败')
        flash('用户注册失败')
        return redirect(url_for('register_view'))


@app.route('/profile/<username>')
def profile(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    posts = u.posts
    comments = u.comments
    activities = posts + comments
    activities.sort(key=lambda a: a.created_time, reverse=True)
    return render_template('profile.html',
                           user=u,
                           activities=activities)

