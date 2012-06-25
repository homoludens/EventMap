# Hello Flask

Simple Event Map Flask web application, including SQLAlchemy, WTForms and Bootstrap, OAuth, and more...

## Demo

http://mfogleman.webfactional.com/hello/

# Installation

## Setting up virual envirement
    
    sudo pip install virtualenv
    $ . venv/bin/activatevirtualenv venv
    $ . venv/bin/activate

## Exit virtualenv
    $ deactivate
    
## Install Dependencies
    
    pip install -r requires
    
##  Start application

    python main.py
   
## Customizations
    Change this in __init__.py for reseting password:
      
    MAIL_USERNAME = 'your.mail@gmail.com',
    MAIL_PASSWORD = 'your.password',

## Modules

Although it is possible for a Flask app to be contained entirely within a single Python module, this project splits different functionality into different modules to facilitate maintainability. Below is a description of each module.

- `__init__.py` - Constructs the Flask app object and configures it. Imports the other modules to emulate a single-module application.
- `config.py` - Contains the app configuration.
- `forms.py` - Contains WTForms Form objects for use in views and templates.
- `hooks.py` - Contains Flask and Jinja helper methods.
- `models.py` - Contains the database model classes for SQLAlchemy.
- `views.py` - Contains the app views.

## Running

    python main.py

## Screenshot

![](https://raw.github.com/fogleman/HelloFlask/master/screenshot.png)
