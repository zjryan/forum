# encoding: utf-8

from . import Model
from . import db

import time


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

    def black_list(self):
        new_bl = [
            'user_id',
            'post_id',
        ]
        self.default_black_list += new_bl
        return self.default_black_list

    def update_dict(self):
        from . import User
        from . import Post
        d = dict(
            author=User.user_by_id(self.user_id).json(),
            post=Post.post_by_id(self.post_id).json()
        )
        return d
