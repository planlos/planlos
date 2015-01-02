# coding: utf-8
from flask import render_template
from .. import factory
from .. import assets
from .context import *
from .filters import *

from .users import mod as users
from .events import mod as events
from .locations import mod as locations
# from .tools import mod as tools
from flask.ext.assets import Bundle


def create_app(settings_override=None):
    app = factory.create_app(__name__, '/',
                             settings_override,
                             static_path="/static",
                             static_url_path="/static",
                             static_folder="frontend/static")

    assets.init_app(app)
    js = Bundle('foundation-sass/js/foundation/foundation.js',
                'foundation-sass/js/foundation/foundation.abide.js',
                'foundation-sass/js/foundation/foundation.accordion.js',
                'foundation-sass/js/foundation/foundation.alert.js',
                'foundation-sass/js/foundation/foundation.clearing.js',
                'foundation-sass/js/foundation/foundation.dropdown.js',
                'foundation-sass/js/foundation/foundation.equalizer.js',
                'foundation-sass/js/foundation/foundation.interchange.js',
                'foundation-sass/js/foundation/foundation.joyride.js',
                'foundation-sass/js/foundation/foundation.magellan.js',
                'foundation-sass/js/foundation/foundation.offcanvas.js',
                'foundation-sass/js/foundation/foundation.orbit.js',
                'foundation-sass/js/foundation/foundation.reveal.js',
                'foundation-sass/js/foundation/foundation.slider.js',
                'foundation-sass/js/foundation/foundation.tab.js',
                'foundation-sass/js/foundation/foundation.tooltip.js',
                'foundation-sass/js/foundation/foundation.topbar.js',
                'foundation-sass/js/vendor/fastclick.js',
                'foundation-sass/js/vendor/jquery.cookie.js',
                'foundation-sass/js/vendor/jquery.js',
                'foundation-sass/js/vendor/modernizr.js',
                'foundation-sass/js/vendor/placeholder.js',
                'foundation-sass/js/app.js',
                output='js/app.js')

    css = Bundle('foundation-sass/css/app.css',
                 output='css/app.css')

    assets.register('js_all', js)
    assets.register('foundation', css)

    app.register_blueprint(events)
    app.register_blueprint(users)
    app.register_blueprint(locations)
    # app.register_blueprint(tools)

    app.errorhandler(404)(not_found)
    app.errorhandler(403)(forbidden)
    app.errorhandler(401)(unauthorized)

    app.context_processor(add_login_form)
    app.context_processor(next_concert)
    app.context_processor(next_demo)
    app.context_processor(add_calendar_view)

    app.template_filter('date')(jinja2_filter_datetime)
    print((app.url_map))
    return app


def not_found(error):
    return render_template('404.html'), 404


def forbidden(error, *args, **kwargs):
    return render_template('403.html'), 403


def unauthorized(error):
    return render_template('401.html'), 401
