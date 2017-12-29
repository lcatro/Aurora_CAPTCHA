# coding: utf8
from tornado.web import RequestHandler


class CustomErrorHandler(RequestHandler):

    def write_error(self, status_code, **kwargs):
        # 405状态码转404
        if status_code == 405:
            status_code = 404
        self.set_status(200)
        self.render('error.html', error=status_code)
