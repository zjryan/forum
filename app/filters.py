# encoding: utf-8

from app import app

import time


@app.template_filter('format_time')
def format_time(timestamp):
    format = '%Y/%m/%d %H:%M:%S'
    t = time.localtime(timestamp)
    ft = time.strftime(format, t)
    return ft


@app.template_filter('from_now')
def format_time(timestamp):
    now = time.time()
    delta_time = now - timestamp
    ret = '{} {}前'
    if delta_time < 5:
        ret = '刚刚'
    elif delta_time < 60:
        ret = ret.format(int(delta_time), '秒')
    elif delta_time < 60 * 60:
        minutes = delta_time / 60
        ret = ret.format(int(minutes), '分钟')
    elif delta_time < 60 * 60 * 24:
        hours = delta_time / 60 / 60
        ret = ret.format(int(hours), '小时')
    elif delta_time < 60 * 60 * 24 * 30:
        days = delta_time / 60 / 60 / 24
        ret = ret.format(int(days), '天')
    elif delta_time < 60 * 60 * 24 * 365:
        mouths = delta_time / 60 / 60 / 24 / 30
        ret = ret.format(int(mouths), '月')
    else:
        years = delta_time / 60 / 60 / 24 / 365
        ret = ret.format(int(years), '年')
    return ret