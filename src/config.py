# coding: utf-8
import os
import logging
import hashlib

from common import functions
from handlers import error
from route import getRoutes


# SITE CONFIG #
SITE_SETTINGS = {
    'host': 'localhost',
    'port': 8081,
    'settings': {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
        'static_url_prefix': '/statics/',
        'default_handler_class': error.CustomErrorHandler,
        'cookie_secret': hashlib.sha1(os.urandom(24)).hexdigest(),
        'xsrf_cookies': False,
        'gzip': True,
        'debug': True,
        'autoreload': True # 在 DEBUG模式下，自动检测代码变更并重启服务
    },
    # SSL CONFIG #
    """
    通常情况下不建议在 Tornado中配置 SSL。在有条件的情况下推荐在前端部署 Nginx来代理 HTTP(S)请求。
        # EXAMPLE #
        'ssl': {
            'certfile': '/root/server.crt',
            'keyfile': '/root/server.key'
        }
    """
    'ssl': None
}

# APPLICATION CONFIG #
APPLICATION_SETTINGS = {

    # DATABASE CONFIG #
    'database': {

    },

    # SMTP CONFIG #
    'smtp': {
        'host': '',
        'port': 498,
        'user': '',
        'pass': '',
        'ssl': True
    },

    # LOGGING CONFIG #
    'logging': logging
}

# ROUTE CONFIG #
routes = getRoutes({
    'functions': functions,
    'logging': APPLICATION_SETTINGS['logging']
})
