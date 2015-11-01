config = {
    # installed_apps
    'installed_apps': [
        'apps.hello'
    ],

    # application name
    'app_name': 'Appudi',

    # webapp2 sessions
    'secret_key': 'da39a3ee5e6b4b0d3255bfef95601890afd80709',

    # jinja2 templates
    'template_path': [
        'apps/hello/templates',
    ],

    # jinja2 base layout template
    'base_layout': 'base.html',

    # Use a complete Google Analytics code, no just the Tracking ID
    # In config/boilerplate.py there is an example to fill out this value
    'google_analytics_code': '',
}
