# coding: utf8
"""
首页模块
"""

import model
from handlers import base


class IndexHandler(base.BaseHandler):
    def initialize(self, **kwargs):
        super(IndexHandler, self).initialize(**kwargs)
        self._dbOperate = model.Model()

    def get(self, *args, **kwargs):
        self.render('index.html')

    def post(self):
        tick_id = self.get_argument('tick')
        valid_state = self.functions.CAPTCHA.check_tick(tick_id)

        if valid_state:
            guest_code = self.get_argument('guest_code')

            if '514230' == guest_code:
                result = 'Pass Success'
            else:
                result = 'Pass Error'
        else:
            result = 'Captcha Error ..'

        self.write(self.functions.object2Json({
            'status': result
        }))
