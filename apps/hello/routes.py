from webapp2 import Route

import handlers


routes = [
    Route('/hello/', handlers.HelloHandler, name='hello', methods=['GET']),
]
