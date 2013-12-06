# -*- coding: utf-8 -*-
"""
    tardigrade.helpers
    ~~~~~~~~~~~~~~~~~~

    a few helpers that are used for our app

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
import re
from datetime import datetime
from unicodedata import normalize

from flask import session, current_app
from flask.ext.themes2 import render_theme_template

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def render_template(template, **context):
    """
    A helper function that uses the `render_theme_template` function
    without needing to edit all the views
    """
    theme = session.get('theme', current_app.config['DEFAULT_THEME'])
    return render_theme_template(theme, template, **context)


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def time_format(value, format='%Y-%m-%d'):
    """
    Returns a formatted time string
    """
    return value.strftime(format)


def time_since(value):
    """
    Just a interface for `time_delta_format`
    """
    return time_delta_format(value)


def time_delta_format(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default
