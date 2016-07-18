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
