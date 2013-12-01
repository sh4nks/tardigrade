# -*- coding: utf-8 -*-
"""
    tardigrade.views.pastebin
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the blog module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, redirect, url_for, flash
from flask.ext.login import login_required, current_user

from tardigrade.models.blog import Post, Comment
from tardigrade.forms.blog import CommentForm, PostForm
from tardigrade.helpers import render_template

pastebin = Blueprint("blog", __name__)


@pastebin.route("/")
def index():
    posts = Post.query.filter_by(is_global=True).all()
    return render_template("blog/index.html", posts=posts)


@pastebin.route("/post/<int:post_id>", methods=["POST", "GET"])
@pastebin.route("/post/<int:post_id>-<slug>", methods=["POST", "GET"])
def view_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    form = None
    if current_user.is_authenticated():
        form = CommentForm()
        if form.validate_on_submit():
            form.save(current_user, post)
            flash("Your comment has been saved!", "success")
            return redirect(url_for("blog.view_post", post_id=post.id,
                                    slug=post.slug))

    return render_template("blog/post.html", post=post, form=form)


@pastebin.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = form.save(current_user)
        flash("Your post has been saved!", "success")
        return redirect(url_for("blog.view_post", post_id=post.id))

    return render_template("blog/post_form.html", form=form, mode="new")


@pastebin.route("/post/<int:post_id>/edit", methods=["POST", "GET"])
@pastebin.route("/post/<int:post_id>-<slug>/edit", methods=["POST", "GET"])
@login_required
def edit_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    if not post.user_id == current_user.id:
        flash("You are not allowed to delete this post.", "danger")
        return redirect(url_for("blog.index"))

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


@pastebin.route("/post/<int:post_id>/delete")
@pastebin.route("/post/<int:post_id>-<slug>/delete")
@login_required
def delete_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    if not post.user_id == current_user.id:
        flash("You are not allowed to delete this post.", "danger")
        return redirect(url_for("blog.index"))

    post.delete()
    flash("This post has been deleted", "success")
    return redirect(url_for("blog.index"))


@pastebin.route("/post/<int:post_id>/comment/new", methods=["POST", "GET"])
@pastebin.route("/post/<int:post_id>-<slug>/comment/new", methods=["POST", "GET"])
@login_required
def new_comment(post_id):
    post = Post.query.filter_by(id=post_id).first()

    form = CommentForm()
    if form.validate_on_submit():
        form.save(current_user, post)
        flash("Your comment has been saved!", "success")
        return redirect(url_for("blog.view_post", post_id=post.id,
                                slug=post.slug))

    return render_template("blog/comment_form.html", post=post, form=form,
                           mode="new")


@pastebin.route("/comment/<int:comment_id>/edit", methods=["POST", "GET"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment.user_id == current_user.id:
        flash("You are not allowed to edit this comment", "danger")
        return redirect(url_for("blog.view_post", post_id=comment.post.id,
                                slug=comment.post.slug))

    form = CommentForm()
    if form.validate_on_submit():
        comment.save()
        flash("Your comment has been edited.", "success")
        return redirect(url_for("blog.view_post", post_id=comment.post.id,
                                slug=comment.post.slug))
    else:
        form.content.data = comment.content

    return render_template("blog/comment_form.html", form=form, mode="edit")


@pastebin.route("/comment/<int:comment_id>/delete")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment.user_id == current_user.id:
        flash("You are not allowed to delete this post", "danger")
        return redirect(url_for("blog.view_post", post_id=comment.post.id,
                                slug=comment.post.slug))

    comment.delete()
    flash("Your comment has been edited.", "success")
    return redirect(url_for("blog.view_post", post_id=comment.post.id,
                            slug=comment.post.slug))
