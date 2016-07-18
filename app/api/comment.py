from flask import request
from flask import jsonify
from flask import abort
from flask import url_for

from ..models import User
from ..models import current_user
from ..models import Comment
from ..models import Post
from . import api


@api.route('/comment/add', methods=['POST'])
def comment_add():
    user = current_user()
    form = request.get_json()
    comment = Comment(form)
    post_id = form.get('post_id')
    r = {
        'success': False,
        'message': '发表评论失败',
    }
    if user is not None and comment.comment_valid():
        comment.set_post(post_id)
        comment.set_author(user.id)
        comment.save()
        r['success'] = True
        r['message'] = '发表评论成功'
        r['data'] = comment.json()
    print(r)
    return jsonify(r)


@api.route('/comment/delete', methods=['POST'])
def comment_delete():
    user = current_user()
    form = request.get_json()
    comment_id = form.get('comment_id')
    comment = Comment.comment_by_id(comment_id)
    r = {
        'success': True,
        'message': '删除评论成功',
    }
    if user is not None and (user.is_admin() or user is comment.author):
        comment.delete()
    else:
        r['success'] = False
        r['message'] = '删除评论失败'
    print(r)
    return jsonify(r)
