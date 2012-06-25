from setuptools import setup

setup(
    name='Flask Map',
    version='1.0',
    long_description=__doc__,
    packages=['eventmap'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'Flask-Mail', 'flask-login', 'flask-sqlalchemy',
                      'flask-wtforms','itsdangerous', 'flask-bcrypt', 'simplejson',
                      'flask-debugtoolbar', 'flask-admin', 'wtalchemy', 'wtforms-csrf']
) 
