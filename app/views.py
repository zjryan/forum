# encoding: utf-8

from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from .models.channel import Channel
from .models.channel import ChannelPermission
from .models.comment import Comment
from .models.user import User
from .models.user import current_user

from app import app
from app.models.post import Post
from .utilities import log


def url_back(route='index'):
    return request.args.get('next') \
                        or request.referrer \
                        or url_for(route)


@app.route('/')
def index():
    return render_template('index.html')