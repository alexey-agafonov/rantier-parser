#!/usr/bin/env python

from aiohttp import web
from rantier_parser.routes import init_routes


async def init_app() -> web.Application:
    app = web.Application()
    init_routes(app)
    return app


if __name__ == '__main__':
    app = init_app()
