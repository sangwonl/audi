from audi.http.response import JSONResponse

import os
import sys
import json
import importlib
import webapp2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'external'))


class Audi(webapp2.WSGIApplication):
    def __init__(self, debug=True, conf=None):
        super(Audi, self).__init__(debug=debug, config=self._update_conf(conf))
        self._initialize()

    def _update_conf(self, cust_conf):
        from settings import config as audi_config
        for name, value in cust_conf.iteritems():
            if name == 'secret_key':
                audi_config['webapp2_extras.sessions']['secret_key'] = value
            elif name == 'template_path':
                audi_config['webapp2_extras.jinja2']['template_path'] += value
            else:
                audi_config[name] = value
        return audi_config

    def _initialize(self):
        self.router.set_dispatcher(self.__class__.dispatcher)

        if not self.debug:
            from .contrib.error_handler import handle_error
            for status_code in self.config['error_templates']:
                self.error_handlers[status_code] = handle_error

        for app_mod_name in self.config['installed_apps']:
            app_routes = importlib.import_module('%s.routes' % app_mod_name)
            for r in app_routes.routes:
                self.router.add(r)

    @staticmethod
    def dispatcher(router, request, response):
        if request.headers.get('Content-Type') == 'application/json':
            request.json = json.loads(request.body)

        rv = router.default_dispatcher(request, response)
        if isinstance(rv, basestring):
            rv = webapp2.Response(rv)
        elif isinstance(rv, tuple):
            rv = webapp2.Response(*rv)
        elif isinstance(rv, dict) or isinstance(rv, list):
            rv = JSONResponse(rv)
        return rv

    @classmethod
    def create_app(cls, conf):
        assert conf is not None

        env_sw = 'SERVER_SOFTWARE'
        is_debug = env_sw not in os.environ or os.environ[env_sw].startswith('Dev')
        return cls(debug=is_debug, conf=conf)
