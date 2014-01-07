# -*- coding: utf-8 -*-
import os


class DefaultConfig(object):
    # Get the app root path
    basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                           os.path.dirname(__file__)))))

    PROJECT = "tardigrade"
    DEBUG = False
    TESTING = False

    # Default Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/' + \
                              PROJECT + ".sqlite"
    # sqlite for testing/debug.
    SQLALCHEMY_ECHO = False

    # Security
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # Protection against form post fraud
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    # Auth
    LOGIN_VIEW = "auth.login"
    REAUTH_VIEW = "auth.reauth"
    LOGIN_MESSAGE_CATEGORY = "danger"

    # Caching
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 60

    ## Captcha
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "your_public_recaptcha_key"
    RECAPTCHA_PRIVATE_KEY = "your_private_recaptcha_key"
    RECAPTCHA_OPTIONS = {"theme": "white"}

    ## Mail
    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = "noreply@example.org"
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = ("Default Sender", "noreply@example.org")
    ADMINS = ["admin@example.org"]

    # Language
    BABEL_DEFAULT_LOCALE = 'en'
    AVAILABLE_LANGUAGES = {"en": "English", "de": "German"}

    # The default theme
    DEFAULT_THEME = "tardigrade"

    # Pastebin settings
    LINE_NUMBERS = False
    # If you change this, you'll also need to change the css variable
    CSS_CLASS = "codehilite"
