# encoding: utf-8

from app import app
from app.models.user import current_user
from app.models.channel import Channel
from app.models.channel import ChannelPermission
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment


@app.context_processor
def current_user_processor():
    return dict(current_user=current_user())


@app.context_processor
def channel_processor():
    channels = Channel.query.all()
    permissions = [
        ChannelPermission.NORMAL,
        ChannelPermission.ADMIN,
    ]
    dic = {
        'channels': channels,
        'permissions': permissions,
    }
    return dict(**dic)


@app.context_processor
def user_processor():
    user_count = User.query.count()
    new_user = User.query.order_by(User.created_time.desc()).first()
    return dict(new_user=new_user,
                user_count=user_count)


@app.context_processor
def post_processor():
    post_count = Post.query.count()
    return dict(post_count=post_count)


@app.context_processor
def comment_processor():
    comment_count = Comment.query.count()
    return dict(comment_count=comment_count)
