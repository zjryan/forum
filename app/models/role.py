# encoding: utf-8

from . import Model
from . import db


class Permission:
    READ = 0x01
    COMMENT = 0x02
    WRITE_POSTS = 0x04
    ADMINISTER = 0x80


class Role(db.Model, Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role')

    def __init__(self, name):
        super(Role, self).__init__()
        self.name = name

    @staticmethod
    def create_roles():
        roles = {
            'GENERAL_USER': (Permission.READ |
                             Permission.COMMENT |
                             Permission.WRITE_POSTS, True),
            'ADMIN': (0xff , False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            role.save()


