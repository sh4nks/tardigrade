# -*- coding: utf-8 -*-
"""
    tardigrade.forms.user
    ~~~~~~~~~~~~~~~~~~~~~

    It provides the forms that are needed for the user views.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, DateField, SelectField
from wtforms.validators import (Required, Optional, Email, URL, EqualTo, regexp,
                                ValidationError)
from flask.ext.babel import lazy_gettext as _

from tardigrade.extensions import db
from tardigrade.models.user import User


IMG_RE = r'^[^/\\]\.(?:jpg|gif|png)'

is_image = regexp(IMG_RE,
                  message=("Only jpg, jpeg, png and gifs are allowed!"))


class ChangeEmailForm(Form):
    old_email = TextField(_("Old E-Mail Address"), validators=[
        Required(message=_("Email adress required")),
        Email(message=_("This email is invalid"))])

    new_email = TextField(_("New E-Mail Address"), validators=[
        Required(message=_("Email adress required")),
        Email(message=_("This email is invalid"))])

    confirm_new_email = TextField(_("Confirm E-Mail Address"), validators=[
        Required(message=_("Email adress required")),
        Email(message=_("This email is invalid")),
        EqualTo("new_email", message=_("E-Mails do not match"))])

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def validate_email(self, field):
        user = User.query.filter(db.and_(
                                 User.email.like(field.data),
                                 db.not_(User.id == self.user.id))).first()
        if user:
            raise ValidationError("This email is taken")


class ChangePasswordForm(Form):
    old_password = PasswordField(_("Old Password"), validators=[
        Required(message=_("Password required"))])

    new_password = PasswordField(_("New Password"), validators=[
        Required(message=_("Password required"))])

    confirm_new_password = PasswordField(_("Confirm New Password"), validators=[
        Required(message=_("Password required")),
        EqualTo("new_password", message=_("Passwords do not match"))])


class ChangeUserDetailsForm(Form):
    birthday = DateField(_("Your Birthday"), format="%d %m %Y", validators=[
        Optional()])

    gender = SelectField(_("Gender"), default="None", choices=[
        ("None", ""),
        ("Male", _("Male")),
        ("Female", _("Female"))])

    firstname = TextField(_("Firstname"), validators=[
        Optional()])

    lastname = TextField(_("Lastname"), validators=[
        Optional()])

    location = TextField(_("Location"), validators=[
        Optional()])

    website = TextField(_("Website"), validators=[
        Optional(), URL()])

    avatar = TextField(_("Avatar"), validators=[
        Optional(), URL()])


class ChangeOtherForm(Form):
    # The choices for those fields will be generated in the user view
    # because we cannot access the current_app outside of the context
    language = SelectField(_("Language"))
    theme = SelectField(_("Theme"))
