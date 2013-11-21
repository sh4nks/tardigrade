# INTRODUCTION

coming soon!


## DEPENDENCIES

* [Flask](http://flask.pocoo.org)
* [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
* [Flask-WTF](http://pythonhosted.org/Flask-WTF/)
* [Flask-Login](http://flask-login.readthedocs.org/en/latest/)
* [Flask-Themes2](http://flask-themes2.readthedocs.org/en/latest/)
* [Flask-Cache](http://pythonhosted.org/Flask-Cache/)
* [Flask-Mail](http://pythonhosted.org/flask-mail/)
* [Flask-Script](http://flask-script.readthedocs.org/en/latest/)


## INSTALLATION

* Create a virtualenv
* Install the dependencies with `pip install -r requirements.txt`
* Copy `tardigrade/settings.py.example` to `tardigrade/settings.py`
* Create the database with some example content `python manage.py createall`
* Run the development server `python manage.py runserver`
* Visit [localhost:8080](http://localhost:8080)


### How to set up a virtualenv with virtualenvwrapper

* Install virtualenvwrapper with your package manager or via
    * `sudo pip install virtualenvwrapper`

* Add these lines to your `.bashrc`

        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/Devel
        source /usr/local/bin/virtualenvwrapper.sh

* Create a new virtualenv
    * `mkvirtualenv -a /path/to/your/project -p $(which python2) projectname`

* and finally activate it
    * `workon projectname`


## LICENSE

[BSD LICENSE](http://flask.pocoo.org/docs/license/#flask-license)
