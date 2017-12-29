# coding: utf8
"""
验证码校验模块
"""

import model
from handlers import base


class getCaptchaHandler(base.BaseHandler):
    def initialize(self, **kwargs):
        super(getCaptchaHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model()

    def get(self):
        return_json = self.functions.CAPTCHA.get_captcha()

        self.write(self.functions.object2Json(return_json))


class validCaptchaHandler(base.BaseHandler):
    def initialize(self, **kwargs):
        super(validCaptchaHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model()

    def post(self):
        tick_id = self.get_argument('tick')
        magic = self.get_argument('magic')
        pow_list = self.get_argument('pow_list')
        pow_list = self.functions.json2Object(pow_list)

        for pow_index in pow_list:
            pow_index['data'] = self.functions.base64Encode(pow_index['data'])
            pow_index['data'] = self.functions.base64Encode(pow_index['data'])

        valid_tick, ignore_magic = self.functions.CAPTCHA.valid_captcha(tick_id, magic, pow_list)

        self.write(self.functions.object2Json({
            'tick': valid_tick
        }))
