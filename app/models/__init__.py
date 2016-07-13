from .. import db


class Model(object):
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


from .channel import Channel
from .channel import ChannelPermission
from .comment import Comment
from .user import User
from .user import current_user
from .post import Post
from .role import Role
