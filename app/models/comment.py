# encoding: utf-8

from . import Model
from . import db

from sqlalchemy import sql


class Comment(db.Model, Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, form):
        super(Comment, self).__init__()
        self.content = form.get('content', '')

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