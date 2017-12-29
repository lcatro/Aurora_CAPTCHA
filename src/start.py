# coding: utf-8
import tornado.web
import tornado.httpserver
import tornado.ioloop

import config


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, config.routes, **config.SITE_SETTINGS['settings'])


def main():
    server = tornado.httpserver.HTTPServer(Application(), ssl_options=config.SITE_SETTINGS.get('ssl', None))
    server.listen(config.SITE_SETTINGS['port'], config.SITE_SETTINGS['host'])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
