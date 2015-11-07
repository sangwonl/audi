# *-* coding: UTF-8 *-*
import json
import webapp2


class JSONResponse(webapp2.Response):
    def __init__(self, data=None):
        super(JSONResponse, self).__init__()
        self.headers['Cache-Control'] = 'no-cache'
        self.headers['Content-Type'] = 'application/json'

        json_dumped = json.dumps(data or {})
        super(JSONResponse, self).write(json_dumped)

