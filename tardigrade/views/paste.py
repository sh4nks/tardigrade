# -*- coding: utf-8 -*-
"""
    tardigrade.views.paste
    ~~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the blog module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from tardigrade.models.paste import Bin
from tardigrade.forms.paste import BinForm
from tardigrade.helpers import render_template

paste = Blueprint("paste", __name__)


@paste.route("/", methods=["POST", "GET"])
def index():
    return new_bin()


@paste.route("/bin/<int:bin_id>", methods=["POST", "GET"])
@paste.route("/bin/<int:bin_id>-<slug>", methods=["POST", "GET"])
def view_bin(bin_id, slug=None):

    pastebin = Bin.query.filter_by(id=bin_id).first()
    form = None

    # User Pygments here to highlight syntax in HTML output
    bincontent = highlight(pastebin.content, PythonLexer(), HtmlFormatter())

    # The following sends the styleinfo to the template as well
    style = HtmlFormatter().get_style_defs('.highlight')

    return render_template("paste/bin.html", pastebin=pastebin, form=form, style=style, bincontent=bincontent)


@paste.route("/bin/new", methods=["POST", "GET"])
@login_required
def new_bin():
    form = BinForm()

    if form.validate_on_submit():
        pastebin = form.save(current_user)
        flash("Your paste-bin has been saved!", "success")
        return redirect(url_for("paste.view_bin", bin_id=pastebin.id))

    return render_template("paste/bin_form.html", form=form, mode="new")


@paste.route("/bin/<int:bin_id>/edit", methods=["POST", "GET"])
@paste.route("/bin/<int:bin_id>-<slug>/edit", methods=["POST", "GET"])
@login_required
def edit_bin(bin_id, slug=None):
    pastebin = Bin.query.filter_by(id=bin_id).first()

    if not pastebin.user_id == current_user.id:
        flash("You are not allowed to delete this paste-bin.", "danger")
        return redirect(url_for("paste.index"))

    form = BinForm()
    if form.validate_on_submit():
        form.save(current_user)
        flash("This paste-bin has been edited", "success")
        return redirect(url_for("paste.view_bin", bin_id=pastebin.id,
                                slug=pastebin.slug))
    else:
        form.description.data = pastebin.description
        form.content.data = pastebin.content

    return render_template("paste/bin_form.html", pastebin=pastebin, form=form,
                           mode="edit")


@paste.route("/bin/<int:bin_id>/delete")
@paste.route("/bin/<int:bin_id>-<slug>/delete")
@login_required
def delete_bin(bin_id, slug=None):
    pastebin = Bin.query.filter_by(id=bin_id).first()

    if not pastebin.user_id == current_user.id:
        flash("You are not allowed to delete this Paste-Bin.", "danger")
        return redirect(url_for("paste.index"))

    pastebin.delete()
    flash("This bin has been deleted", "success")
    return redirect(url_for("paste.index"))
