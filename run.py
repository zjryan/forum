# encoding: utf-8

from app import init_app


app = init_app()


if __name__ == '__main__':
    debug = True
    app.run(debug=debug)