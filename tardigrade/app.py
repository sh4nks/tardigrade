# -*- coding: utf-8 -*-
"""
    tardigrade.app
    ~~~~~~~~~~~~~~

    manages the app creation and configuration process

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
import datetime

from flask import Flask, request
from flask.ext.login import current_user

from tardigrade.models.user import User
# import the bluepritns
from tardigrade.views.auth import auth
from tardigrade.views.user import user
from tardigrade.views.blog import blog
from tardigrade.views.paste import paste
from tardigrade.extensions import (db, login_manager, mail, cache, babel,
                                   themes, misaka, debugtoolbar)
from tardigrade.helpers import (render_template, time_format, time_since,
                                can_modify, highlighter)


DEFAULT_BLUEPRINTS = (
    (auth, ""),
    (user, "/user"),
    (blog, ""),
    (paste, "/paste")
)


def create_app(config=None, blueprints=None):
    """
    Creates the app.
    """

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    # Initialize the app
    app = Flask("tardigrade")

    app.config.from_object("tardigrade.configs.default")
    if config:
        app.config.from_object(config)

    configure_extensions(app)
    configure_blueprints(app, blueprints)
    configure_template_filters(app)
    configure_before_handlers(app)
    configure_errorhandlers(app)

    return app


def configure_extensions(app):
    """
    Configures the extensions
    """

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Mail
    mail.init_app(app)

    # Flask-Cache
    cache.init_app(app)

    # Flask-Themes2
    themes.init_themes(app, app_identifier="tardigrade")

    # Flask-Debugtoolbar
    debugtoolbar.init_app(app)

    # Flask-Misaka
    misaka.init_app(app)

    # Flask-Login
    login_manager.login_view = app.config["LOGIN_VIEW"]
    login_manager.refresh_view = app.config["REAUTH_VIEW"]

    @login_manager.user_loader
    def load_user(id):
        """
        Loads the user. Required by the `login` extension
        """
        return User.query.get(id)

    login_manager.init_app(app)

    # Flask-Babel
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        if current_user.is_authenticated() and current_user.language:
            return current_user.language
        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/en in this
        # example. The best match wins.
        return request.accept_languages.\
            best_match(app.config["AVAILABLE_LANGUAGES"].keys())


def configure_blueprints(app, blueprints):
    """
    Configures the blueprints
    """

    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_template_filters(app):
    """
    Configures the template filters
    """
    app.jinja_env.filters['highlighter'] = highlighter
    app.jinja_env.filters['time_format'] = time_format
    app.jinja_env.filters['time_since'] = time_since
    app.jinja_env.filters['can_modify'] = can_modify


def configure_before_handlers(app):
    """
    Configures the before request handlers
    """

    @app.before_request
    def update_lastseen():
        """
        Updates `lastseen` before every reguest if the user is authenticated
        """
        if current_user.is_authenticated():
            current_user.lastseen = datetime.datetime.utcnow()
            db.session.add(current_user)
            db.session.commit()


def configure_errorhandlers(app):
    """
    Configures the error handlers
    """

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500
