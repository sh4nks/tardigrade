# -*- coding: utf-8 -*-
"""
    tardigrade.views.blog
    ~~~~~~~~~~~~~~~~~~~~~

    The views that are used by the blog module

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, redirect, url_for, flash, abort
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from tardigrade.models.blog import Post, Comment
from tardigrade.forms.blog import CommentForm, PostForm
from tardigrade.helpers import render_template, can_modify

# This will create a blueprint named `blog`
# to make it available in other blueprints for example when you want to use
# url_for("blog.index"), you need to register it at the flask instance
# you can do it like this `app.register_blueprint` - see app.py
blog = Blueprint("blog", __name__)


# Now you can access the blueprint via `blog`
@blog.route("/")
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("blog/index.html", posts=posts)


@blog.route("/post/<int:post_id>", methods=["POST", "GET"])
@blog.route("/post/<int:post_id>-<slug>", methods=["POST", "GET"])
def view_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    # abort if no post is found
    if not post:
        abort(404)

    # if you do not initialize the form, it will raise an error when user is
    # not registered
    form = None
    # check if the current user is authenticated
    if current_user.is_authenticated():
        # assign the `form` variable the `CommentForm` class
        form = CommentForm()

        # check if the form has any errors and is a `POST` request
        if form.validate_on_submit():
            # save the post
            form.save(current_user, post)
            flash(_("Your comment has been saved!"), "success")

            # and finally redirect to the post
            return redirect(url_for("blog.view_post", post_id=post.id,
                                    slug=post.slug))

    return render_template("blog/post.html", post=post, form=form)


@blog.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = form.save(current_user)
        flash(_("Your post has been saved!"), "success")
        return redirect(url_for("blog.view_post", post_id=post.id))

    return render_template("blog/post_form.html", form=form, mode="new")


@blog.route("/post/<int:post_id>/edit", methods=["POST", "GET"])
@blog.route("/post/<int:post_id>-<slug>/edit", methods=["POST", "GET"])
@login_required
def edit_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    # abort if no post is found
    if not post:
        abort(404)

    # check if the user has the right permissions to edit this post
    if not can_modify(post, current_user):
        flash(_("You are not allowed to delete this post."), "danger")
        return redirect(url_for("blog.index"))

    form = PostForm()
    if form.validate_on_submit():
        # this will update the changed attributes
        form.populate_obj(post)
        post.save()
        flash(_("This post has been edited"), "success")
        return redirect(url_for("blog.view_post", post_id=post.id,
                                slug=post.slug))
    else:
        form.title.data = post.title
        form.content.data = post.content

    return render_template("blog/post_form.html", post=post, form=form,
                           mode="edit")


@blog.route("/post/<int:post_id>/delete")
@blog.route("/post/<int:post_id>-<slug>/delete")
@login_required
def delete_post(post_id, slug=None):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        abort(404)

    if not can_modify(post, current_user):
        flash(_("You are not allowed to delete this post."), "danger")
        return redirect(url_for("blog.index"))

    post.delete()
    flash(_("This post has been deleted", "success"))
    return redirect(url_for("blog.index"))


@blog.route("/post/<int:post_id>/comment/new", methods=["POST", "GET"])
@blog.route("/post/<int:post_id>-<slug>/comment/new", methods=["POST", "GET"])
@login_required
def new_comment(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        abort(404)

    form = CommentForm()
    if form.validate_on_submit():
        form.save(current_user, post)
        flash(_("Your comment has been saved!"), "success")
        return redirect(url_for("blog.view_post", post_id=post.id,
                                slug=post.slug))

    return render_template("blog/comment_form.html", post=post, form=form,
                           mode="new")


@blog.route("/comment/<int:comment_id>/edit", methods=["POST", "GET"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        abort(404)

    if not can_modify(comment, current_user):
        flash(_("You are not allowed to edit this comment"), "danger")
        return redirect(url_for("blog.view_post", post_id=comment.post.id,
                                slug=comment.post.slug))

    form = CommentForm()
    if form.validate_on_submit():
        form.populate_obj(comment)
        comment.save()
        flash(_("Your comment has been edited."), "success")
        return redirect(url_for("blog.view_post", post_id=comment.post.id,
                                slug=comment.post.slug))
    else:
        form.content.data = comment.content

    return render_template("blog/comment_form.html", form=form, mode="edit")


@blog.route("/comment/<int:comment_id>/delete")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        abort(404)

    if not can_modify(comment, current_user):
        flash(_("You are not allowed to delete this post"), "danger")
        return redirect(url_for("blog.view_post", post_id=comment.post.id,
                                slug=comment.post.slug))
    post = comment.post
    comment.delete()
    flash(_("Your comment has been edited."), "success")
    return redirect(url_for("blog.view_post", post_id=post.id, slug=post.slug))
