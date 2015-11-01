config = {
    # installed_apps
    'installed_apps': [],

    # application name
    'app_name': '',

    # the default language code for the application.
    # should match whatever language the site uses when i18n is disabled
    'app_lang': 'en',

    # Locale code = <language>_<territory> (ie 'en_US')
    # to pick locale codes see http://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code
    # also see http://www.sil.org/iso639-3/codes.asp
    # Language codes defined under iso 639-1 http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    # Territory codes defined under iso 3166-1 alpha-2 http://en.wikipedia.org/wiki/ISO_3166-1
    # disable i18n if locales array is empty or None
    'locales': ['en_US', 'es_ES', 'it_IT', 'zh_CN', 'id_ID', 'fr_FR', 'de_DE', 'ru_RU', 'pt_BR', 'cs_CZ', 'vi_VN', 'nl_NL'],

    # add status codes and templates used to catch and display errors
    # if a status code is not listed here it will use the default app engine
    # stacktrace error page or browser error page
    'error_templates': {
        403: 'errors/default_error.html',
        404: 'errors/default_error.html',
        500: 'errors/default_error.html',
    },

    # webapp2 sessions
    'webapp2_extras.sessions': {'secret_key': ''},

    # webapp2 authentication
    'webapp2_extras.auth': {'user_model': 'audi.apps.auth.models.User', 'cookie_name': 'session'},

    # jinja2 templates
    'webapp2_extras.jinja2': {
        'environment_args': {'extensions': ['jinja2.ext.i18n']},
        'template_path': [
            'audi/apps/common/templates'
        ]
    },

    # jinja2 base layout template
    'base_layout': 'base.html',
}

