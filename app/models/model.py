# encoding: utf-8

from flask import Flask
from app import db


app = Flask(__name__)
app.secret_key = 'ert4-bgs6-3rew-hj9x'


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

