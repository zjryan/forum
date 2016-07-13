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