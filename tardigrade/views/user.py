# -*- coding: utf-8 -*-
"""
    tardigrade.views.user
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the user module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint
from flask.ext.babel import gettext as _

user = Blueprint("user", __name__)


@user.route("/me")
def profile():
    return _("Hello Me!")
