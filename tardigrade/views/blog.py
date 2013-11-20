# -*- coding: utf-8 -*-
"""
    tardigrade.views.blog
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the blog module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint

blog = Blueprint("blog", __name__)


@blog.route("/")
def index():
    return "Hello Blog!"
