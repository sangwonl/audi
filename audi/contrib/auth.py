import uuid
import jwt


class BaseAuthenticator(object):
    def __init__(self, *args, **kwargs):
        pass

    def authenticate(self, request):
        raise NotImplemented

    def create_token(self):
        raise NotImplemented


class JWTAuthenticator(BaseAuthenticator):
    def __init__(self, *args, **kwargs):
        super(JWTAuthenticator, self).__init__(*args, **kwargs)
        self.algorithm = kwargs.get('algorithm', 'HS256')
        self.secret = kwargs.get('secret', uuid.uuid4().hex)
        self.issuer = kwargs.get('issuer', '')

    def authenticate(self, request):
        hdr_key = 'Authorization'
        if hdr_key not in request.headers:
            return None

        authorization = request.headers[hdr_key]
        if authorization is None or authorization == '':
            return None

        token = authorization.replace('Bearer', '').strip()
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        if payload is None or 'iss' not in payload or payload['iss'] != self.issuer:
            return None

        return payload

    def create_token(self, email=None, expire=None):
        payload = {'iss': self.issuer}
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)


