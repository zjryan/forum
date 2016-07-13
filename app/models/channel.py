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