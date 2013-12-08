# -*- coding: utf-8 -*-
"""
    tardigrade.models.paste
    ~~~~~~~~~~~~~~~~~~~~~~

    This module provides the models for the paste-bin.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from tardigrade.extensions import db
from tardigrade.helpers import slugify


class Bin(db.Model):
    __tablename__ = "bin"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    description = db.Column(db.String)
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    @property
    def slug(self):
        return slugify(self.description)

    def save(self, user=None):
        # Update the bin
        if self.id:
            db.session.add(self)
            db.session.commit()
            return self

        # Create a new bin
        if user:
            self.user_id = user.id

            db.session.add(self)
            db.session.commit()
            return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
