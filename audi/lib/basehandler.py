# *-* coding: UTF-8 *-*
from babel import Locale
from webapp2_extras import jinja2, auth, sessions
from audi.lib import utils, i18n, jinja_bootstrap

import pytz
import webapp2


class BaseHandler(webapp2.RequestHandler):
    """
    BaseHandler for all requests

    Holds the auth and session properties so they
    are reachable for all requests
    """

    def __init__(self, request, response):
        super(BaseHandler, self).__init__(request, response)
        self.initialize(request, response)
        self.locale = i18n.set_locale(self, request)
        self.session_store = None

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            # csrf protection
            if self.request.method == 'POST':
                token = self.session.get('csrf_token')
                if not token or (token != self.request.get('csrf_token') and
                    token != self.request.headers.get('csrf_token')):
                    self.abort(403)

            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def user(self):
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user_model(self):
        return self.auth.store.user_model

    @webapp2.cached_property
    def user_id(self):
        return str(self.user['user_id']) if self.user else None

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    @webapp2.cached_property
    def language(self):
        return str(Locale.parse(self.locale).language)

    @property
    def locales(self):
        """
        returns a dict of locale codes to locale display names in both the current locale and the localized locale
        example: if the current locale is es_ES then locales['en_US'] = 'Ingles (Estados Unidos) - English (United States)'
        """
        if not self.app.config.get('locales'):
            return None
        locales = {}
        for l in self.app.config.get('locales'):
            current_locale = Locale.parse(self.locale)
            language = current_locale.languages[l.split('_')[0]]
            territory = current_locale.territories[l.split('_')[1]]
            localized_locale_name = Locale.parse(l).display_name.capitalize()
            locales[l] = language.capitalize() + ' (' + territory.capitalize() + ') - ' + localized_locale_name
        return locales

    @webapp2.cached_property
    def tz(self):
        tz = [(tz, tz.replace('_', ' ')) for tz in pytz.all_timezones]
        tz.insert(0, ('', ''))
        return tz

    @webapp2.cached_property
    def get_user_tz(self):
        user = self.current_user
        if user:
            if hasattr(user, 'tz') and user.tz:
                return pytz.timezone(user.tz)
        return pytz.timezone('UTC')

    @webapp2.cached_property
    def countries(self):
        return Locale.parse(self.locale).territories if self.locale else []

    @webapp2.cached_property
    def countries_tuple(self):
        countries = self.countries
        if '001' in countries:
            del (countries['001'])
        countries = [(key, countries[key]) for key in countries]
        countries.append(('', ''))
        countries.sort(key=lambda tup: tup[1])
        return countries

    @webapp2.cached_property
    def current_user(self):
        user = self.auth.get_user_by_session()
        if user:
            return self.user_model.get_by_id(user['user_id'])
        return None

    @webapp2.cached_property
    def is_mobile(self):
        return utils.set_device_cookie_and_return_bool(self)

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja_bootstrap.jinja2_factory, app=self.app)

    @webapp2.cached_property
    def get_base_layout(self):
        """
        Get the current base layout template for jinja2 templating. Uses the variable base_layout set in config
        or if there is a base_layout defined, use the base_layout.
        """
        return self.base_layout if hasattr(self, 'base_layout') else self.app.config.get('base_layout')

    def render_template(self, filename, **kwargs):
        locales = self.app.config.get('locales') or []
        locale_iso = None
        language = ''
        territory = ''
        language_id = self.app.config.get('app_lang')

        if self.locale and len(locales) > 1:
            locale_iso = Locale.parse(self.locale)
            language_id = locale_iso.language
            territory_id = locale_iso.territory
            language = locale_iso.languages[language_id]
            territory = locale_iso.territories[territory_id]

        # set or overwrite special vars for jinja templates
        kwargs.update({
            'google_analytics_code': self.app.config.get('google_analytics_code'),
            'app_name': self.app.config.get('app_name'),
            'url': self.request.url,
            'path': self.request.path,
            'query_string': self.request.query_string,
            'is_mobile': self.is_mobile,
            'locales': self.locales,
            'locale_iso': locale_iso,
            'locale_language': language.capitalize() + ' (' + territory.capitalize() + ')',
            'locale_language_id': language_id,
            'base_layout': self.get_base_layout
        })

        self.response.headers.add_header('X-UA-Compatible', 'IE=Edge,chrome=1')
        self.response.write(self.jinja2.render_template(filename, **kwargs))
