# -*- coding: utf-8 -*-
"""
    tardigrade.views.user
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the user module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, abort, current_app, url_for, redirect, session
from flask.ext.themes2 import get_themes_list

from tardigrade.models.user import User
from tardigrade.helpers import render_template


user = Blueprint("user", __name__)


@user.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return render_template("user/profile.html", user=user)


@user.route("/settings")
def settings():
    return "Settings Page"


@user.route("/settings/themes")
def themes():
    themes = get_themes_list()
    return render_template("user/themes.html", themes=themes)


@user.route('/settings/themes/<ident>')
def set_theme(ident):
    if ident not in current_app.theme_manager.themes:
        abort(404)
    session['theme'] = ident
    return redirect(url_for('user.themes'))
