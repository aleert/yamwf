# -*- coding: utf-8 -*-

from webob import Request

from yamwf.routing import load_controller


def app(environ, start_response):
    req = Request(environ)
    resp = load_controller(req, req.path)
    return resp(environ, start_response)
