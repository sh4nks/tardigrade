# -*- coding: utf-8 -*-
"""
    tardigrade.forms.auth
    ~~~~~~~~~~~~~~~~~~~~~

    It provides the forms that are needed for the auth views.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField
from wtforms.validators import Required, Email, EqualTo, regexp, ValidationError, Length
from flask.ext.babel import lazy_gettext as _

from tardigrade.models.user import User

USERNAME_RE = r"^[\w.+-]+$"
is_username = regexp(USERNAME_RE,
                     message=(_("You may only use letters, numbers or dashes")))


class LoginForm(Form):
    login = TextField(_("Username or E-Mail"), validators=[
        Required(message=_("You must provide an email adress or username"))])

    password = PasswordField(_("Password"), validators=[
        Required(message=_("Password required"))])

    remember_me = BooleanField(_("Remember Me"), default=False)


class RegisterForm(Form):
    username = TextField(_("Username"), validators=[
        Required(message=_("Username required")),
        is_username])

    email = TextField(_("E-Mail"), validators=[
        Required(message=_("Email adress required")),
        Email(message=_("Invalid Email address"))])

    password = PasswordField(_("Password"), validators=[
        Required(message=_("Password required")), Length(min=5)])

    confirm_password = PasswordField(_("Confirm Password"), validators=[
        Required(message=_("Confirm Password required")),
        EqualTo("password", message=_("Passwords do not match"))])

    accept_tos = BooleanField(_("Accept Terms of Service"), 
        default=False, validators=[
        Required(message=_("You have to accept the Terms of Service"))])

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError(_("This username is already taken"))

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError(_("This e-Mail is already taken"))

    def save(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data,
                    date_joined=datetime.utcnow())
        return user.save()


class ReauthForm(Form):
    password = PasswordField(_("Password"), [Required()])


class ForgotPasswordForm(Form):
    email = TextField(_("Email"), validators=[
        Required(message=_("Email reguired")),
        Email()])


class ResetPasswordForm(Form):
    token = HiddenField("Token")

    email = TextField(_("Email"), validators=[
        Required(),
        Email()])

    password = PasswordField(_("Password"), validators=[
        Required()])

    confirm_password = PasswordField(_("Confirm password"), validators=[
        Required(),
        EqualTo("password", message=_("Passwords do not match"))])

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if not email:
            raise ValidationError(_("Wrong e-Mail address."))
