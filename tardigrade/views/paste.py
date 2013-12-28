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
from flask.ext.babel import gettext as _
from pygments import highlight
from pygments.lexers import (PythonLexer, CppLexer, JavaLexer, XmlLexer,
                             HtmlLexer)
from pygments.formatters import HtmlFormatter

from tardigrade.models.paste import Bin
from tardigrade.forms.paste import BinForm
from tardigrade.helpers import render_template, can_modify

paste = Blueprint("paste", __name__)


@paste.route("/", methods=["POST", "GET"])
def index():
    public_pastes = Bin.query.filter_by(is_public=True).all()
    return render_template("paste/index.html", pastes=public_pastes)


@paste.route("/bin/<int:bin_id>", methods=["POST", "GET"])
def view_bin(bin_id, slug=None):

    pastebin = Bin.query.filter_by(id=bin_id).first()
    form = None

    # User Pygments here to highlight syntax in HTML output
    #Check which highlighting to user
    #Python has no real "switch" :( so lets use a dictionary
    # None is default
    lexer = {
        'Text': None,
        'C++': CppLexer(),
        'Java': JavaLexer(),
        'HTML': HtmlLexer(),
        'Python': PythonLexer(),
        'XML': XmlLexer()
    }.get(pastebin.lang, None)

    if lexer:
        bincontent = highlight(pastebin.content, lexer, HtmlFormatter())
    else:
        bincontent = "<pre> {} </pre>".format(pastebin.content)

    # The following sends the styleinfo to the template as well
    style = HtmlFormatter().get_style_defs('.highlight')

    #Check if post is private and send user to login
    #if yes and user not logged in
    if not pastebin.is_public and not current_user.is_authenticated():
        return redirect(url_for("auth.login"))

    else:
        return render_template("paste/bin.html", pastebin=pastebin, form=form,
                               style=style, bincontent=bincontent)


@paste.route("/bin/new", methods=["POST", "GET"])
@login_required
def new_bin():
    form = BinForm()

    if form.validate_on_submit():
        pastebin = form.save(current_user)
        flash(_("Your paste-bin has been saved!"), "success")
        return redirect(url_for("paste.view_bin", bin_id=pastebin.id))

    return render_template("paste/bin_form.html", form=form, mode="new")


@paste.route("/bin/<int:bin_id>/edit", methods=["POST", "GET"])
@paste.route("/bin/<int:bin_id>-<slug>/edit", methods=["POST", "GET"])
@login_required
def edit_bin(bin_id, slug=None):
    pastebin = Bin.query.filter_by(id=bin_id).first()

    #Edit is more or less the same as creating a new one
    #You can not actually overwrite the existing one
    #You can just generate a new edited copy of it
    #Every user can edit a pastebin because you do not override the original one

    #Default Language is the one of the original (current/to edit) post
    form = BinForm(lang=pastebin.lang)
    if form.validate_on_submit():
        pastebin = form.save(current_user)
        flash(_("Your paste-bin has been saved!"), "success")
        return redirect(url_for("paste.view_bin", bin_id=pastebin.id))
    else:
        form.description.data = "{}*".format(pastebin.description)
        form.content.data = pastebin.content

    return render_template("paste/bin_form.html", pastebin=pastebin, form=form,
                           mode="edit")


@paste.route("/bin/<int:bin_id>/delete")
@paste.route("/bin/<int:bin_id>-<slug>/delete")
@login_required
def delete_bin(bin_id, slug=None):
    pastebin = Bin.query.filter_by(id=bin_id).first()

    if not can_modify(pastebin, current_user):
        flash(_("You are not allowed to delete this Paste-Bin."), "danger")
        return redirect(url_for("paste.index"))

    pastebin.delete()
    flash(_("This bin has been deleted"), "success")
    return redirect(url_for("paste.index"))
