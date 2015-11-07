from audi import Audi
from settings import config

import unittest
import webtest


class AppTest(unittest.TestCase):
    def setUp(self):
        app = Audi.create_app(config)
        self.testapp = webtest.TestApp(app)

    def testHelloWorldHandler(self):
        response = self.testapp.get('/hello/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'text/html')
        self.assertTrue('Hello World' in response.normal_body)
