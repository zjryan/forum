from . import auth
from flask import redirect
from flask import render_template
from flask import url_for


@auth.route('/')
def index():
    return render_template('login.html')