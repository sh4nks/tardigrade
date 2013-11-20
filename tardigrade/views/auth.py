# -*- coding: utf-8 -*-
"""
    tardigrade.views.auth
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the auth module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return "Login!"


@auth.route("/register")
def register():
    return "Registration!"


@auth.route("/forgotpassword")
def forgot_password():
    return "Forgot Password!"
