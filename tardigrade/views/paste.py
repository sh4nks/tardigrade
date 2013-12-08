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

from tardigrade.models.paste import Bin
from tardigrade.forms.paste import BinForm
from tardigrade.helpers import render_template

paste = Blueprint("paste", __name__)


@paste.route("/")
def index():
    return new_bin()


@paste.route("/bin/<int:post_id>", methods=["POST", "GET"])
@paste.route("/bin/<int:post_id>-<slug>", methods=["POST", "GET"])
def view_bin(post_id, slug=None):

    post = Post.query.filter_by(id=post_id).first()
    form = None
    return render_template("paste/bin.html", post=post, form=form)


@paste.route("/bin/new", methods=["POST", "GET"])
@login_required
def new_bin():
    form = BinForm()

    if form.validate_on_submit():
        post = form.save(current_user)
        flash("Your paste-bin has been saved!", "success")
        return redirect(url_for("paste.view_bin", post_id=post.id))

    return render_template("paste/bin_form.html", form=form, mode="new")


@paste.route("/bin/<int:post_id>/edit", methods=["POST", "GET"])
@paste.route("/bin/<int:post_id>-<slug>/edit", methods=["POST", "GET"])
@login_required
def edit_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    if not post.user_id == current_user.id:
        flash("You are not allowed to delete this post.", "danger")
        return redirect(url_for("paste.index"))

    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user)
        flash("This post has been edited", "success")
        return redirect(url_for("blog.view_post", post_id=post.id,
                                slug=post.slug))
    else:
        form.title.data = post.title
        form.content.data = post.content

    return render_template("blog/post_form.html", post=post, form=form,
                           mode="edit")


@paste.route("/bin/<int:post_id>/delete")
@paste.route("/bin/<int:post_id>-<slug>/delete")
@login_required
def delete_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    if not post.user_id == current_user.id:
        flash("You are not allowed to delete this post.", "danger")
        return redirect(url_for("blog.index"))

    post.delete()
    flash("This post has been deleted", "success")
    return redirect(url_for("blog.index"))
