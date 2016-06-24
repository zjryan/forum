# encoding: utf-8

from . import Model
from . import db

from sqlalchemy import sql


class Post(db.Model, Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())

    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='post')

    def __init__(self, form):
        super(Post, self).__init__()
        self.title = form.get('title', '')
        self.content = form.get('content', '')

    def post_valid(self):
        return self.title != '' and self.content != ''

    def set_channel(self, channel_id):
        self.channel_id = channel_id

    def set_author(self, user_id):
        self.user_id = user_id