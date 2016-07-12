# encoding: utf-8

from . import Model
from . import db

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
        return self.title != '' and self.content != ''

    def set_channel(self, channel_id):
        self.channel_id = channel_id

    def set_author(self, user_id):
        self.user_id = user_id

    def display_item(self):
        name = 'post'
        title = self.title
        content_len = 58
        if self.content.__len__() > content_len:
            content = self.content[:content_len] + '...'
        else:
            content = self.content
        return (name, title, content)