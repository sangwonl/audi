from audi.core.handlers.base import BaseHandler


class HelloHandler(BaseHandler):
    def get(self):
        return self.render_template('hello.html')
