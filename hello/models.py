from hello import db, app
from datetime import datetime
from flaskext.bcrypt import Bcrypt

from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)

#from flask_dashed.admin import Admin
#from flask_dashed.ext.sqlalchemy import ModelAdminModule, model_form

from flask.ext import admin, wtf
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import filters


from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import aliased, contains_eager

from werkzeug import OrderedMultiDict
from  forms import SignupForm, CommentForm

from wtforms import validators

bcrypt = Bcrypt()

        
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    pwdhash = db.Column(db.String())
    email = db.Column(db.String(60))
    fb_id = db.Column(db.String(30), unique=True)
    activate = db.Column(db.Boolean)
    created = db.Column(db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.pwdhash = bcrypt.generate_password_hash(password)
        #self.pwdhash = password
        self.email = email
        self.activate = True
        self.created = datetime.utcnow()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwdhash, password)


     #def __init__(self, username, uid, activate=True):
        #self.name = username
        #self.id = uid
        #self.activate = activate

    def is_active(self):
        return self.activate

    def get_id(self):
        return  self.uid

    def __unicode__(self):
        return self.username


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    text2 = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Numeric, nullable=True)
    latitude = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.Date, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    user = db.relationship('Users',
                        primaryjoin='Users.uid == Comment.uid',
                        backref=db.backref('users', lazy='joined'))

    def __init__(self, text, text2, longitude, latitude, date, timestamp, uid):
        self.text = text
        self.text2 = text2
        self.longitude = longitude
        self.latitude = latitude
        self.date = date
        self.timestamp = timestamp
        self.uid = uid
        
    def __unicode__(self):
        return self.text

# Customized Post model admin
class CommentAdmin(sqla.ModelView):
    # Visible columns in the list view
    #list_columns = ('title', 'user')
    #excluded_list_columns = ['text']

    # List of columns that can be sorted. For 'user' column, use User.username as
    # a column.
    sortable_columns = ('text', 'uid','timestamp')

    # Rename 'title' columns to 'Post Title' in list view
    rename_columns = dict(title='Comment Title')

    searchable_columns = ('text', Comment.text)

    column_filters = ('uid',
                      'text',
                      'timestamp',
                      filters.FilterLike(Comment.text, 'Fixed Title', options=(('test1', 'Test 1'), ('test2', 'Test 2'))))

    # Pass arguments to WTForms. In this case, change label for text field to
    # be 'Big Text' and add required() validator.
    form_args = dict(
                    text=dict(label='Big Text', validators=[validators.Required()])
                )

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(CommentAdmin, self).__init__(Comment, session)


# Create admin
admin = admin.Admin(app, 'Event Map Admin')

# Add views
admin.add_view(sqla.ModelView(Users, db.session))
admin.add_view(CommentAdmin(db.session))