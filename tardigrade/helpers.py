# -*- coding: utf-8 -*-
"""
    tardigrade.helpers
    ~~~~~~~~~~~~~~~~~~

    a few helpers that are used for our app

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import session, current_app
from flask.ext.themes2 import render_theme_template


def render_template(template, **context):
    theme = session.get('theme', current_app.config['DEFAULT_THEME'])
    return render_theme_template(theme, template, **context)
