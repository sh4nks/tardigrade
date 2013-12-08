# -*- coding: utf-8 -*-
"""
    tardigrade.forms.paste
    ~~~~~~~~~~~~~~~~~~~~~~

    It provides the forms that are needed for the paste views.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, Length
from flask.ext.babel import lazy_gettext as _

from tardigrade.models.paste import Bin


class BinForm(Form):
    description = TextField(_("Description"), validators=[
        Required(message=_("Please enter a short discription/title for your paste-bin!")),
        Length(min=0, max=140)])

    content = TextAreaField(_("Content"), validators=[
        Required(message=_("You can't create a pase-bin without content"))])

    def save(self, user):
        post = Post(**self.data)
        return post.save(user=user)

