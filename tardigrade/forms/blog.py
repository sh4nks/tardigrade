# -*- coding: utf-8 -*-
"""
    tardigrade.forms.auth
    ~~~~~~~~~~~~~~~~~~~~~

    It provides the forms that are needed for the auth views.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, Length
from flask.ext.babel import lazy_gettext as _

from tardigrade.models.blog import Post, Comment


class PostForm(Form):
    title = TextField(_("Title"), validators=[
        Required(message=_("A title is required")),
        Length(min=0, max=140)])

    content = TextAreaField(_("Content"), validators=[
        Required(message=_("You can't submit a post without content"))])

    def save(self, user):
        post = Post(**self.data)
        return post.save(user=user)


class CommentForm(Form):
    content = TextAreaField(_("Comment"), validators=[
        Required(message=_("You can't submit a comment without content"))])

    def save(self, user):
        comment = Comment(**self.data)
        return comment.save(user=user)
