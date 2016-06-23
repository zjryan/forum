# encoding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'ert4-bgs6-3rew-hj9x'
db_path = '../models.db'
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///{}'.format(db_path)

db = SQLAlchemy(app)


from app import views