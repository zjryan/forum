# encoding: utf-8

from . import Model
from . import db
from . import Channel
from . import User

import time


class Post(db.Model, Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='post')

    def __init__(self, form):
        super(Post, self).__init__()
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = time.time()

    def post_valid(self):
        message = '发表帖子成功'
        has_title = len(self.title) > 0
        valid_content = len(self.content) >= 10
        if not has_title:
            message = '帖子标题不能为空'
        elif not valid_content:
            message = '帖子长度必须不小于10个字符'
        status = has_title and valid_content
        return status, message

    def set_channel(self, channel_id):
        self.channel_id = channel_id

    def set_author(self, user_id):
        self.user_id = user_id

    @staticmethod
    def post_by_id(id):
        return Post.query.get(id)

    def black_list(self):
        new_bl = [
            'user_id',
            'channel_id',
            'comments'
        ]
        self.default_black_list += new_bl
        return self.default_black_list

    def update_dict(self):
        d = dict(
            author=User.user_by_id(self.user_id).json(),
            channel=Channel.channel_by_id(self.channel_id).json(),
            link='url_for("controller.post_view", id={})'.format(self.id)
        )
        return d