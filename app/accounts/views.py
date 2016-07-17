from . import accounts
from flask import session
from flask import render_template
from flask import url_for
from flask import request
from flask import jsonify
from flask import redirect
from ..models import User
from ..decorators import login_required
from ..utilities import log


@accounts.route('/')
def index():
    return render_template('login.html')


@accounts.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    username = form.get('username', '')
    user = User.user_by_name(username)

    r = {
        'success': False,
        'message': '登录失败',
    }
    if user is not None and user.login_valid(form):
        r['success'] = True
        r['next'] = request.args.get('next', url_for('index'))
        r['message'] = '登录成功'
        session.permanent = True
        session['user_id'] = user.id
    else:
        r['success'] = False
        r['message'] = '登录失败'
    print(r)
    return jsonify(r)


@accounts.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


@accounts.route('/register', methods=['POST'])
def register():
    form = request.get_json()
    success, message = User.register_valid(form)

    r = {
        'success': True,
        'message': message,
    }
    if success:
        user = User(form)
        user.save()
        log('注册成功')
        r['success'] = True
        r['next'] = request.args.get('next', url_for('index'))
        session.permanent = True
        session['user_id'] = user.id
    else:
        log('注册失败', form)
        r['success'] = False
    return jsonify(r)
