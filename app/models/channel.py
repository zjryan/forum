# encoding: utf-8

from . import Model
from . import db

import time


class ChannelPermission:
    NORMAL = 0x01
    ADMIN = 0x80


class Channel(db.Model, Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), default=ChannelPermission.NORMAL)
    permission = db.Column(db.Integer)
    created_time = db.Column(db.Integer, default=0)

    posts = db.relationship('Post', backref='channel')

    def __init__(self, form):
        super(Channel, self).__init__()
        self.name = form.get('name', '')
        self.permission = form.get('permission', ChannelPermission.NORMAL)
        self.created_time = time.time()

    @staticmethod
    def add_valid(form):
        channel_name = form.get('name', '')
        length = len(channel_name)
        return length > 2 and length <= 15

    def is_admin(self):
        return self.permission == ChannelPermission.ADMIN

    @staticmethod
    def channel_by_id(id):
        return Channel.query.get_or_404(id)

    @staticmethod
    def posts_sorted_by_time(posts, reverse=True):
        posts.sort(key=lambda p: p.created_time, reverse=reverse)
        return posts

    def black_list(self):
        self.default_black_list.append('posts')
        return self.default_black_list

    def update_dict(self):
        d = dict(
            link='/channel/{}'.format(self.id)
        )
        return d
