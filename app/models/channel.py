# encoding: utf-8

from . import Model
from . import db

from sqlalchemy import sql


class Channel(db.Model, Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())

    def __init__(self, form):
        super(Channel, self).__init__()
        self.name = form.get('name', '')