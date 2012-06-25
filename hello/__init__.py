from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.mail import Mail, Message

#from flask_dashed.admin import Admin
#from flask_dashed.ext.sqlalchemy import ModelAdminModule, model_form
#from models import UserModule

#mail = Mail()

app = Flask(__name__)
app.config.from_object('hello.config')
app.secret_key = 'A0Zr98j/3yX R~XHH!'
app.debug = 0
app.config.update(
        DEBUG=False,
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'your.email@gmail.com',
        MAIL_PASSWORD = 'your.pass',
        MAIL_DEBUG = 0
        )

mail = Mail(app)

#mail = Mail()
#mail.init_app(app)

db = SQLAlchemy(app)

import hooks
import models
import views
