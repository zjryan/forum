# encoding: utf-8

from . import Model
from . import db

from sqlalchemy import sql


class Post(db.Model, Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())

    def __init__(self, form):
        super(Post, self).__init__()
        self.content = form.get('content', '')
