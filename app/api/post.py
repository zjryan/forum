from flask import request
from flask import jsonify
from flask import abort

from ..models import User
from ..models import current_user
from ..models import Post
from . import api


@api.route('/post/add', methods=['POST'])
def post_add():
    user = current_user()
    form = request.get_json()
    post = Post(form)
    channel_id = form.get('channel_id')
    success, message = post.post_valid()
    r = {
        'success': False,
        'message': message,
    }
    if success:
        r['success'] = True
        post.set_author(user.id)
        post.set_channel(channel_id)
        post.save()
        r['data'] = post.json()
    print(r)
    return jsonify(r)


@api.route('/post/delete', methods=['POST'])
def post_delete():
    user = current_user()
    form = request.get_json()
    post_id = form.get('post_id')
    post = Post.post_by_id(post_id)
    r = {
        'success': False,
        'message': '删除失败'
    }

    if post is None:
        abort(404)
    if user is not None or post.author is user or user.is_admin():
        r['success'] = True
        r['message'] = '删除成功'
        post.delete()
    else:
        abort(401)
    print(r)
    return jsonify(r)


@api.route('/post', methods=['POST'])
def post_full():
    form = request.get_json()
    post_id = form.get('post_id')
    post = Post.post_by_id(post_id)
    data = post.content
    r = {
        'success': True,
        'message': '获取帖子成功',
        'data': data,
    }
    print(r)
    return jsonify(r)


