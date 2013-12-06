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
import datetime

from flask import current_app
from flask.ext.script import Manager, Shell, Server

from tardigrade import create_app
from tardigrade.configs.development import DevelopmentConfig
from tardigrade.extensions import db
from tardigrade.models.user import User
from tardigrade.models.blog import Post, Comment


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
    """
    Creates the database with some example content
    """
    # Just for testing purposes
    dbfile = os.path.join(DevelopmentConfig.basedir, "tardigrade.sqlite")
    if os.path.exists(dbfile):
        os.remove(dbfile)

    db.create_all()

    user1 = User(username="test1", password="test", email="test@example.org",
                 theme=current_app.config["DEFAULT_THEME"],
                 language=current_app.config["BABEL_DEFAULT_LOCALE"])
    user1.save()

    user2 = User(username="test2", password="test", email="test2@example.org",
                 theme="bootstrap2",
                 language="de")

    user2.save()

    post = Post(title="Example 1", content="Example Content",
                date_created=datetime.datetime.utcnow())
    post.save(user1)

    comment = Comment(content="Test Comment",
                      date_created=datetime.datetime.utcnow())
    comment.save(user2, post)


@manager.command
def update_translations():
    """
    Updates the translations
    """
    os.system("pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .")
    os.system("pybabel update -i messages.pot -d tardigrade/translations")
    os.unlink("messages.pot")


@manager.command
def init_translations(translation):
    """
    Adds a new language to the translations
    """
    os.system("pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .")
    os.system("pybabel init -i messages.pot -d tardigrade/translations -l " + translation)
    os.unlink('messages.pot')


@manager.command
def compile_translations():
    """
    Compiles the translations.
    """
    os.system("pybabel compile -d tardigrade/translations")


if __name__ == "__main__":
    manager.run()
