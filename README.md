# INTRODUCTION

Tardigrade is a tiny content-management environment.

We developed it as a project for a course at our university.
These are the requirements our product has to fulfill:

* persistent data
* XML or JSON web services for AJAX
* authentication and registration with double opt-in
* no passwords stored as plain text
* user input validation
* i18n (optional)

A demo version is online at [cansee.at](http://cansee.at).

## DEPENDENCIES

* [Flask](http://flask.pocoo.org)
* [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
* [Flask-WTF](http://pythonhosted.org/Flask-WTF/)
* [Flask-Login](http://flask-login.readthedocs.org/en/latest/)
* [Flask-Themes2](http://flask-themes2.readthedocs.org/en/latest/)
* [Flask-Cache](http://pythonhosted.org/Flask-Cache/)
* [Flask-Mail](http://pythonhosted.org/flask-mail/)
* [Flask-Script](http://flask-script.readthedocs.org/en/latest/)
* [Pygments](http://pygments.org)


## INSTALLATION

* Create a virtualenv
* Install the dependencies with `pip install -r requirements.txt`
* Configuration (_adjust them accordingly to your needs_)
    * For development copy `tardigrade/development.py.example` to `tardigrade/development.py`
    * For production copy `tardigrade/production.py.example` to `tardigrade/production.py`
* Create the database with some example content `python manage.py createall`
* Run the development server `python manage.py runserver`
* Visit [localhost:8080](http://localhost:8080)


### How to set up a virtualenv with virtualenvwrapper

* Install virtualenvwrapper with your package manager or via
    * `sudo pip install virtualenvwrapper`

* Add these lines to your `.bashrc`

        export WORKON_HOME=$HOME/.virtualenvs  # Location for your virtualenvs
        source /usr/local/bin/virtualenvwrapper.sh

* Create a new virtualenv
    * `mkvirtualenv -a /path/to/your/project -p $(which python2) projectname`

* and finally activate it
    * `workon projectname`

For more options visit the documentation [here](http://virtualenvwrapper.readthedocs.org/en/latest/index.html).

## LICENSE

[BSD LICENSE](http://flask.pocoo.org/docs/license/#flask-license)
