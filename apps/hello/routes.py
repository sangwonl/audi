from webapp2_extras.routes import RedirectRoute

import handlers


routes = [
    RedirectRoute('/hello/', handlers.HelloHandler, name='hello', strict_slash=True),
]
