# encoding: utf-8

from . import Model
from . import db
from .role import Role
from .role import Permission
from ..utilities import email_validate
from ..utilities import generate_password_hash
from ..utilities import check_password_hash

from sqlalchemy import sql
from flask import session


class User(db.Model, Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    created_time = db.Column(db.DateTime(timezone=True),
                             default=sql.func.now())

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
        return self.role.permissions == Permission.ADMINISTER

    def can_read(self):
        return self.role.permissions & Permission.READ

    def can_comment(self):
        return self.role.permissions & Permission.COMMENT

    def can_write_post(self):
        return self.role.permissions & Permission.WRITE_POSTS


def current_user():
    id = session.get('user_key', None)

    user = None
    if id is not None:
        user = User.query.get(id)
    return user
