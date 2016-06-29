# encoding: utf-8

from app import app

import time


@app.template_filter('format_time')
def format_time(timestamp):
    format = '%Y/%m/%d %H:%M:%S'
    t = time.localtime(timestamp)
    ft = time.strftime(format, t)
    return ft