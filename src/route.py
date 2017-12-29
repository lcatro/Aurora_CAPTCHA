# coding: utf-8
from tornado.web import url

from handlers.index.handler import *
from handlers.captcha.handler import *


def getRoutes(options):
    routes = []

    # <-- INDEX MODULE --> #
    routes.extend([url(r'^/$', IndexHandler, dict(options), name='Index')  # 首页
                   ])

    # <-- CAPTCHA MODULE --> #
    routes.extend([url(r'^/get_captcha$', getCaptchaHandler, dict(options), name='getCaptcha'),  # 获取验证码接口
                   url(r'^/valid_captcha$', validCaptchaHandler, dict(options), name='validCaptcha')  # 验证接口
                   ])

    return routes
