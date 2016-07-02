# encoding: utf-8

from .model import Model
from .model import db

import time
import json


class Comment(db.Model, Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, form):
        super(Comment, self).__init__()
        self.content = form.get('content', '')
        self.created_time = time.time()

    def comment_valid(self):
        return self.content != ''

    def set_author(self, user_id):
        self.user_id = user_id

    def set_post(self, post_id):
        self.post_id = post_id

    def display_item(self):
        name = 'comment'
        if self.content.__len__() > 30:
            content = self.content[:30] + '...'
        else:
            content = self.content
        return (name, content)

    def dict(self, **kwargs):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'author': self.author.dict(kwargs.get('size', 60)),
        }
        return d

    def json(self):
        d = self.dict()
        return json.dumps(d)