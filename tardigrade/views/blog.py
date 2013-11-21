# -*- coding: utf-8 -*-
"""
    tardigrade.views.blog
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the blog module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, current_app, redirect, url_for, abort, session
from flask.ext.themes2 import get_themes_list

from tardigrade.helpers import render_template

blog = Blueprint("blog", __name__)


@blog.route("/")
def index():
    themes = get_themes_list()
    return render_template('themes.html', themes=themes)


@blog.route('/themes/<ident>')
def settheme(ident):
    if ident not in current_app.theme_manager.themes:
        abort(404)
    session['theme'] = ident
    return redirect(url_for('blog.index'))
