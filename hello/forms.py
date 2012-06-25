from flask.ext.wtf import Form, TextField, DecimalField, TextAreaField, DateField, validators, PasswordField, BooleanField

class CommentForm(Form):
    text = TextField('Title', [validators.Required()])
    text2 = TextAreaField('Body')
    longitude = DecimalField('Longitude')
    latitude = DecimalField('Longitude')
    date = DateField('Date')


class SignupForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [validators.Required()])
    email = TextField('eMail', [validators.Required(),validators.Email()])
    #accept_tos = BooleanField('I accept the TOS', [validators.Required])


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class PasswordResetForm(Form):
    username = TextField('Username')
    email = TextField('eMail')

class PasswordChangeForm(Form):
    password = PasswordField('Password', [validators.Required()])
