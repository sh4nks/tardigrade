# -*- coding: utf-8 -*-
"""
    tardigrade.views.user
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the user module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, abort

from tardigrade.models.user import User
from tardigrade.helpers import render_template


user = Blueprint("user", __name__)


@user.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return render_template("user.html")


@user.route("/settings")
def settings():
    return "Settings Page"
