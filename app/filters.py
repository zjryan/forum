# encoding: utf-8

from app import app


@app.template_filter
def length(container):
    return len(container)