/**
 * Created by Gabriel on 2016/7/11.
 */

// log
var log = function () {
    console.log(arguments);
};

// form
var formFromKeys = function (keys, prefix) {
    var form = {};
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var tagid = prefix + key;
        var value = $('#' + tagid).val();
        if (value.length < 1) {
            break;
        }
        form[key] = value;
    }
    return form;
};

var alertMessage = function (msg) {
    html = '<div class="alert alert-danger" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
            msg + '</div>';
    $('#id-div-alert').append(html);
};

var dismissAlert = function () {
    $('#id-div-alert').empty();
};

var formatTime = function (timestamp) {
    var time = new Date(timestamp * 1000);
    var add0 = function (x) {
        return x < 10 ? '0' + x.toString() : x;
    };
    var year = time.getFullYear();
    var month = time.getMonth() + 1;
    var day = time.getDate();
    var hour = time.getHours();
    var minute = time.getMinutes();
    var second = time.getSeconds();

    return year + '/' + add0(month) + '/' + add0(day) + ' ' + add0(hour) + ':' + add0(minute) + ':' + add0(second);
};

var fromNow = function (timestamp) {
    var now = new Date().getTime() / 1000;
    var delta_time = now - timestamp;
    var ret = '{} {}前';
    if (delta_time < 10) {
        ret = '刚刚';
    } else if (delta_time < 60){
        ret = Math.floor(delta_time).toString() + '秒';
    } else if (delta_time < 60 * 60) {
        var minutes = delta_time / 60;
        ret = Math.floor(minutes).toString() + '分钟';
    } else if (delta_time < 60 * 60 * 24) {
        var hours = delta_time / 60 / 60;
        ret = Math.floor(hours).toString() + '小时';
    } else if (delta_time < 60 * 60 * 24 * 30) {
        var days = delta_time / 60 / 60 / 24;
        ret = Math.floor(days).toString() + '天';
    } else if (delta_time < 60 * 60 * 24 * 365) {
        var mouths = delta_time / 60 / 60 / 24 / 30;
        ret = Math.floor(mouths).toString() + '月';
    } else {
        var years = delta_time / 60 / 60 / 24 / 365;
        ret = Math.floor(years).toString() + '年';
    }
    return ret;
};

var bbs = {
    data: {}
};

bbs.ajax = function (url, method, form, success, error) {
    var request = {
        url: url,
        type: method,
        contentType: 'application/json',
        success: function (r) {
            log('bbs post success', url, r);
            success(r);
        },
        error: function (err) {
            r = {
                success: false,
                data: err
            };
            log('bbs post err', url, err);
            error(r);
        }
    };
    if (method === 'post') {
        var data = JSON.stringify(form);
        request.data = data;
    }
    $.ajax(request);
};

bbs.get = function (url, response) {
    var method = 'get';
    var form = {};
    this.ajax(url, method, form, response, response);
};

bbs.post = function(url, form, success, error) {
    var method = 'post';
    this.ajax(url, method, form, success, error);
};

bbs.register = function(form, success, error) {
    var url = '/accounts/register';
    this.post(url, form, success, error);
};

bbs.login = function(form, success, error) {
    var url = '/accounts/login';
    this.post(url, form, success, error);
};

bbs.postAdd = function (form, success, error) {
    var url = '/api/post/add';
    this.post(url, form, success, error);
};

bbs.postDelete = function (form, success, error) {
    var url = '/api/post/delete';
    this.post(url, form, success, error);
};

bbs.getPost = function (form, success, error) {
    var url = '/api/post';
    this.post(url, form, success, error);
};

bbs.commentAdd = function (form, success, error) {
    var url = '/api/comment/add';
    this.post(url, form, success, error);
};