# -*- coding: utf-8 -*-

"""Main app. Import your controllers to activate them."""
from wsgiref.simple_server import make_server

from yamwf.wsgi import app as wsgi_app

try:
    from example_app import controllers
except ImportError:
    raise ImportError('Cannot load controllers for example_app.')


if __name__ == '__main__':
    with make_server('', 8080, wsgi_app) as httpd:
        print("Serving HTTP on port 8080...")

        # Respond to requests until process is killed
        httpd.serve_forever()
