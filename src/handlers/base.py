# coding: utf-8
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    db = None
    functions = None
    logging = None

    def initialize(self, **kwargs):
        if kwargs:
            self.functions = kwargs.get('functions')
            self.logging = kwargs.get('logging')

    @property
    def getUserIP(self):
        return self.request.remote_ip

    def get_login_url(self):
        return self.reverse_url('login')

    def get_template_namespace(self):
        """
        update namespace
        """
        namespace = super(BaseHandler, self).get_template_namespace()
        name = {
            'sftime': self.functions.formatTime
        }
        namespace.update(name)
        return namespace

    def write_error(self, status_code, **kwargs):
        # 405状态码转404
        if status_code == 405:
            status_code = 404
        self.set_status(200)
        self.render('error.html', error=status_code)
