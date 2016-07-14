from flask import request
from flask import jsonify

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
        r['data'] = post.json()
        post.save()
    print(r)
    return jsonify(r)