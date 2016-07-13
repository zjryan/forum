# encoding: utf-8

from . import Model
from . import db
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

        min_len = 3
        max_len = 12
        username_exists = User.user_by_name(username) is not None
        valid_username_len = len(username) >= min_len and len(username) <= max_len
        valid_password_len = len(password) >= min_len
        identical_password = password == password2
        valid_email = email_validate(email)
        email_exists = User.query.filter_by(email=email).first() is not None

        message = '注册成功'
        if username_exists:
            message = '用户名已经存在'
        elif not valid_username_len:
            message = '用户名长度应不大于{}且不小于{}'.format(max_len, min_len)
        elif not valid_email:
            message = '邮箱格式不正确'
        elif email_exists:
            message = '该邮箱已经被注册'
        elif not identical_password:
            message = '输入的密码不一致'
        elif not valid_password_len:
            message = '密码长度应不小于{}'.format(min_len)
        status = not email_exists and not username_exists and valid_email and \
            valid_password_len and identical_password and valid_username_len
        return status, message

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

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def user_by_id(id):
        return User.query.get_or_404(id)


def current_user():
    id = session.get('user_id', None)
    user = None
    if id is not None:
        user = User.user_by_id(id)
    return user
