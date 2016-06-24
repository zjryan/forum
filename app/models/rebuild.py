# encoding: utf-8

from app.models import rebuild_db
from app.models.role import Role
from app.utilities import log


def create_roles():
    Role.create_roles()
    log('user roles created')


if __name__ == '__main__':
    rebuild_db()
    create_roles()