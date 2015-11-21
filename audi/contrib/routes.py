from webapp2_extras import routes


class AuthRoute(routes.RedirectRoute):
    def __init__(self, template, handler=None, **kwargs):
        class AuthRequiredHandler(handler):
            def __init__(self, request, response):
                super(AuthRequiredHandler, self).__init__(request, response)
                self.auth_required = True

        super(AuthRoute, self).__init__(template, handler=AuthRequiredHandler, **kwargs)

    def match(self, request):
        return super(AuthRoute, self).match(request)

    def build(self, request, args, kwargs):
        return super(AuthRoute, self).build(request, args, kwargs)