# -*- coding: utf-8 -*-
"""
    tardigrade.models.blog
    ~~~~~~~~~~~~~~~~~~~~~~

    This module provides the models for the blog.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from tardigrade.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id",
                                                  ondelete="CASCADE"))
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def save(self, user=None, post=None):
        # Update the comment
        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        if user and post:
            self.user_id = user.id
            self.post_id = post.id

            db.session.add(self)
            db.session.commit()
            return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    comment_count = db.column_property(
        db.select([db.func.count(Comment.id)]).where(Comment.post_id == id).
        as_scalar())

    comments = db.relationship("Comment", backref="post", lazy="dynamic")

    @property
    def slug(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.count()

    def save(self, user=None):
        # Update the post
        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        # Create a new post
        if user:
            self.user_id = user.id

            db.session.add(self)
            db.session.commit()
            return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
