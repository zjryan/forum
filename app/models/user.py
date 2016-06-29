# encoding: utf-8

from .model import Model
from .model import db
from .role import Role
from .role import Permission
from app.utilities import email_validate
from app.utilities import generate_password_hash
from app.utilities import check_password_hash

import time
from flask import session
from hashlib import md5


class User(db.Model, Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    avatar_hash = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='author')

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')
        self.set_user_role()
        self.cache_avatar()
        self.created_time = time.time()

    def login_valid(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        return username == self.username and \
            self.verify_password(password)

    @staticmethod
    def register_valid(form):
        username = form.get('username', '')
        password = form.get('password', '')
        password2 = form.get('password2', '')
        email = form.get('email', '')

        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        username_len = len(username) >= 3
        password_len = len(password) >= 3
        email_valid = email_validate(email)

        return not user_exists and \
               not email_exists and \
               email_valid and \
               password == password2 and \
               password_len and \
               username_len

    def set_user_role(self):
        if self.role_id is None:
            role = Role.query.filter_by(default=True).first()
            self.role_id = role.id

    def is_admin(self):
        return self.role.permissions == 0xff

    def can_read(self):
        return self.role.permissions & Permission.READ

    def can_comment(self):
        return self.role.permissions & Permission.COMMENT

    def can_write_post(self):
        return self.role.permissions & Permission.WRITE_POSTS

    def gravatar(self, size=100, default='identicon', rating='g'):
        from flask import request
        gravatar_url = 'secure.gravatar.com/avatar'
        if request.is_secure:
            url = 'https://' + gravatar_url
        else:
            url = 'http://' + gravatar_url
        hash = self.avatar_hash or md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,
                                                                     hash=hash,
                                                                     size=size,
                                                                     default=default,
                                                                     rating=rating)

    def cache_avatar(self):
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = md5(self.email.encode('utf-8')).hexdigest()


def current_user():
    id = session.get('user_key', None)

    user = None
    if id is not None:
        user = User.query.get(id)
    return user
