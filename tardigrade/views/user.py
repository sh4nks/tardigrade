# -*- coding: utf-8 -*-
"""
    tardigrade.views.user
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the user module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, abort, url_for, redirect, flash, current_app

from flask.ext.themes2 import get_themes_list
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from tardigrade.models.user import User
from tardigrade.forms.user import (ChangeEmailForm, ChangePasswordForm,
                                   ChangeUserDetailsForm, ChangeOtherForm)
from tardigrade.helpers import render_template


user = Blueprint("user", __name__)


@user.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return render_template("user/profile.html", user=user)


@user.route("/<username>/blog")
def userblog(username):
    user = User.query.filter_by(username=username).first()
    return render_template("user/blog.html", posts=user.posts)


@user.route("/settings/")
@login_required
def settings():
    # to be continued
    return redirect(url_for("user.change_other"))


@user.route("/settings/other", methods=["POST", "GET"])
@login_required
def change_other():
    form = ChangeOtherForm()

    form.language.choices = [(locale, name)
                             for locale, name in
                             current_app.config["AVAILABLE_LANGUAGES"].
                             iteritems()]

    form.theme.choices = [(theme.identifier, theme.name)
                          for theme in get_themes_list()]

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()
        flash(_("Your settings have been updated."), "success")
        return redirect(url_for("user.change_other"))
    else:
        form.theme.data = current_user.theme
        form.language.data = current_user.language

    return render_template("user/change_other.html", form=form)


@user.route("/settings/change-email", methods=["POST", "GET"])
def change_email():
    form = ChangeEmailForm(current_user)

    if form.validate_on_submit():
        current_user.email = form.new_email.data
        current_user.save()

        flash(_("Your email has been updated!"), "success")
        return redirect(url_for("user.change_email"))

    return render_template("user/change_email.html", form=form)


@user.route("/settings/change-password", methods=["POST", "GET"])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.password = form.new_password.data
        current_user.save()

        flash(_("Your password has been updated!"), "success")
        return redirect(url_for("user.change_password"))

    return render_template("user/change_password.html", form=form)


@user.route("/settings/change-user-details", methods=["POST", "GET"])
def change_user_details():
    form = ChangeUserDetailsForm()

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()

        flash(_("Your details have been updated!"), "success")
        return redirect(url_for("user.change_user_details"))
    else:
        form.birthday.data = current_user.birthday
        form.gender.data = current_user.gender
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.location.data = current_user.location
        form.website.data = current_user.website
        form.avatar.data = current_user.avatar
        form.about_me.data = current_user.about_me

    return render_template("user/change_user_details.html", form=form)
