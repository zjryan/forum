# encoding: utf-8

from .model import Model
from .model import db

from sqlalchemy import sql


class ChannelPermission:
    NORMAL = (0x01, '普通频道')
    ADMIN = (0x80, '管理员频道')


class Channel(db.Model, Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), default=ChannelPermission.NORMAL[0])
    permission = db.Column(db.Integer)
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())

    posts = db.relationship('Post', backref='channel')

    def __init__(self, form):
        super(Channel, self).__init__()
        self.name = form.get('name', '')
        self.permission = form.get('permission', ChannelPermission.NORMAL[0])

    @staticmethod
    def add_valid(form):
        channel_name = form.get('name', '')
        length = len(channel_name)
        return length > 2 and length < 10

    def is_admin(self):
        return self.permission == ChannelPermission.ADMIN[0]