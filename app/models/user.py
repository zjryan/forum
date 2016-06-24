# encoding: utf-8

from . import Model
from . import db
from ..utilities import email_validate

from sqlalchemy import sql


class User(db.Model, Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String())
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())

    posts = db.relationship('Post', backref='author')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')

    def login_valid(self, user):
        return user is not None and \
            user.username == self.username and \
            user.password == self.password

    @staticmethod
    def register_valid(form):
        username = form.get('username', '')
        password = form.get('password', '')
        email = form.get('email', '')

        user_exists = User.query.filter_by(username=username).first()
        username_len = len(username) >= 3
        password_len = len(password) >= 3
        email_valid = email_validate(email)

        return not user_exists and email_valid and password_len and username_len

