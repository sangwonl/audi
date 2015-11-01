from webapp2_extras.appengine.auth import models
from google.appengine.ext import ndb


class User(models.User):
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    country = ndb.StringProperty()
    tz = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def get_by_email(cls, email):
        return cls.query(cls.email == email).get()
