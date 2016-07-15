from .. import db
import json


class Model(object):
    default_black_list = [
        '_sa_instance_state',
        'default_black_list'
    ]

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = (u'{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return u'\n<{0}:\n  {1}\n'.format(class_name, '\n    '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        self.load_model()
        print(self.__class__.__name__)
        new_d = self.update_dict()
        d = {k: v for k, v in self.__dict__.items() if k not in self.black_list()}
        d.update(new_d)
        return d

    def black_list(self):
        return self.default_black_list

    def update_dict(self):
        return dict()

    def load_model(self):
        self.default_black_list += []

from .channel import Channel
from .channel import ChannelPermission
from .comment import Comment
from .user import User
from .user import current_user
from .post import Post
from .role import Role
