# encoding: utf-8

from flask import Flask


app = Flask(__name__)
app.secret_key = 'jgn3-kigf-4bgk-0ndv'


from app import views
from .models.user import current_user


@app.context_processor
def current_user_processor():
    return dict(current_user=current_user())
