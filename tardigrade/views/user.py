# -*- coding: utf-8 -*-
"""
    tardigrade.views.user
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the user module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint

from tardigrade.helpers import render_template


user = Blueprint("user", __name__)


@user.route("/me")
def profile():
    return render_template("user.html")
