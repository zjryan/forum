var deletePost = function (postId) {
    var selector = '#id-post-item-' + postId;
    console.log(selector);
    $(selector).remove();
};

var deleteCurrentPost = function (postId) {
    var form = {
        'post_id': postId,
    };
    var success = function (r) {
        if (r.success) {
            deletePost(postId);
        } else {
            alertMessage(r.message);
        }
    };
    var error = function (err) {
        log(err);
    };
    bbs.postDelete(form, success, error);
};

var bindPostDelete = function () {
    $('.button-delete').on('click', function () {
        var postId = this.dataset.id;
        dismissAlert();
        deleteCurrentPost(postId);
    });
};
