#!/usr/bin/env python

from rantier_parser.views import index


def init_routes(app):
    app.router.add_get('/', index)
