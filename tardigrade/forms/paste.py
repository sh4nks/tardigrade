# -*- coding: utf-8 -*-
"""
    tardigrade.forms.paste
    ~~~~~~~~~~~~~~~~~~~~~~

    It provides the forms that are needed for the paste views.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField, BooleanField
from wtforms.validators import Required, Length
from flask.ext.babel import lazy_gettext as _

from tardigrade.models.paste import Bin


class BinForm(Form):
    description = TextField(_("Description"), validators=[
        Required(message=_("Please enter a short discription/title for your paste-bin!")),
        Length(min=0, max=140)])

    content = TextAreaField(_("Content"), validators=[
        Required(message=_("You can't create a pase-bin without content"))])

    lang = SelectField(_("Highlighting"),
        choices=[('Text', 'None (Plain Text)'), ('C++', 'C++'), ('HTML', 'HTML'),
                ('Java', 'Java'), ('Python', 'Python'), ('XML', 'XML')])

    is_public = BooleanField(_("Public Bin"), default=False)

    def save(self, user):
        pastebin = Bin(**self.data)
        return pastebin.save(user=user)

