# -*- coding: utf-8 -*-
"""
    tardigrade.extensions
    ~~~~~~~~~~~~~~~~~~~~~

    The extensions that are used by Tardigrade.

    :copyright: (c) 2013 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.cache import Cache
from flask.ext.babel import Babel
from flask.ext.themes2 import Themes
#from flask.ext.debugtoolbar import DebugToolbarExtension

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# Mail
mail = Mail()

# Caching
cache = Cache()

# Babel
babel = Babel()

# Themes
themes = Themes()

# Debugtoolbar
# The Debugtoolbar does not (atm) support the "factory" design
#toolbar = DebugToolbarExtension()
