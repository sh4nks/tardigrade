"""
    tardigrade.manage
    ~~~~~~~~~~~~~~~~~

    This script provides some easy to use commands for
    creating the database and running the development server.
    Just type `python manage.py` to see the full list of commands.

    :copyright: (c) 2013 by the Tardigrade Team.
    :license: BSD, see LICENSE for more details.
"""
import os
from flask import current_app
from flask.ext.script import Manager, Shell, Server

from tardigrade import create_app
from tardigrade.configs.development import DevelopmentConfig
from tardigrade.extensions import db

# Use the development configuration if available
app = create_app(DevelopmentConfig)
manager = Manager(app)

# Run local server
manager.add_command("runserver", Server("localhost", port=8080))


# Add interactive project shell
def make_shell_context():
    return dict(app=current_app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def initdb():
    """
    Creates the database.
    """

    db.create_all()


@manager.command
def createall():
    # Just for testing purposes
    dbfile = os.path.join(DevelopmentConfig.basedir, "tardigrade.sqlite")
    if os.path.exists(dbfile):
        os.remove(dbfile)

    db.create_all()


if __name__ == "__main__":
    manager.run()
