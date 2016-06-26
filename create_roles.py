# encoding: utf-8

from app.models.role import Role
from app.utilities import log


def create_roles():
    Role.create_roles()
    log('user roles created')


if __name__ == '__main__':
    create_roles()