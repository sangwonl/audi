# -*- coding: utf-8 -*-
from audi.core.handlers.base import BaseHandler


class RobotsHandler(BaseHandler):
    def get(self):
        params = {
            'scheme': self.request.scheme,
            'host': self.request.host,
        }
        self.response.headers['Content-Type'] = 'text/plain'

        def set_variables(text, key):
            return text.replace('{{ %s }}' % key, params[key])

        self.response.write(reduce(set_variables, params, open('audi/apps/common/templates/seo/robots.txt').read()))


class HumansHandler(BaseHandler):
    def get(self):
        params = {
            'scheme': self.request.scheme,
            'host': self.request.host,
        }
        self.response.headers['Content-Type'] = 'text/plain'

        def set_variables(text, key):
            return text.replace('{{ %s }}' % key, params[key])

        self.response.write(reduce(set_variables, params, open('audi/apps/common/templates/seo/humans.txt').read()))


class SitemapHandler(BaseHandler):
    def get(self):
        params = {
            'scheme': self.request.scheme,
            'host': self.request.host,
        }
        self.response.headers['Content-Type'] = 'application/xml'

        def set_variables(text, key):
            return text.replace('{{ %s }}' % key, params[key])

        self.response.write(reduce(set_variables, params, open('audi/apps/common/templates/seo/sitemap.xml').read()))


class CrossDomainHandler(BaseHandler):
    def get(self):
        params = {
            'scheme': self.request.scheme,
            'host': self.request.host,
        }
        self.response.headers['Content-Type'] = 'application/xml'

        def set_variables(text, key):
            return text.replace('{{ %s }}' % key, params[key])

        self.response.write(reduce(set_variables, params, open('audi/apps/common/templates/seo/crossdomain.xml').read()))
