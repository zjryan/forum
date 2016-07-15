var briefLen = 100;

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

var shortContent = function (content, len) {
    if (content.length > len) {
        content = content.slice(0, len) + '...';
    }
    return content
};

var displayAll = function (postId, fullData) {
    var selector = '#id-post-content-' + postId;
    $(selector).text(fullData)
};

var displayBrief = function (postId) {
    var selector = '#id-post-content-' + postId;
    var content = $(selector).text();
    content = shortContent(content, briefLen);
    $(selector).text(content);
};

var getFullPost = function (postId) {
    var form = {
        'post_id': postId,
    };
    var success = function (r) {
        if (r.success) {
            displayAll(postId, r.data);
        } else {
            alertMessage(r.message);
        }
    };
    var error = function (err) {
        log(err);
    };
    bbs.getPost(form, success, error);
};

var displaySetUp = function (self) {
    self.next().hide();
    var content = self.prev().text();
    if (content.length > briefLen) {
        content = shortContent(content, briefLen);
        console.log(content);
        self.prev().text(content);
    } else {
        self.hide();
    }
};

var displaySetUpAll = function () {
    $('.display-all').each(function () {
        var self = $(this);
        displaySetUp(self);
    });
};

var displaySetUpFirst = function () {
    var self = $('.post-body .display-all:first');
    displaySetUp(self);
};

var bindDisplayAll = function () {
    $('.display-all').on('click', function () {
        var postId = this.dataset.id;
        var self = $(this);
        dismissAlert();
        getFullPost(postId);
        self.hide();
        self.next().show();
    });
};

var bindDisplayBrief = function () {
    $('.display-brief').on('click', function () {
        var self = $(this);
        var postId = this.dataset.id;
        self.hide();
        dismissAlert();
        displayBrief(postId);
        self.prev().show();
    });
};