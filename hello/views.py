from flask import render_template, url_for, redirect, flash, request, session, g
from forms import CommentForm, SignupForm, LoginForm, PasswordResetForm, PasswordChangeForm
from hello import app, db
from models import Comment, Users
import datetime
from itsdangerous import TimestampSigner, URLSafeSerializer

from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from flaskext.mail import Mail, Message

from flaskext.bcrypt import Bcrypt

from flask_debugtoolbar import DebugToolbarExtension


from flask.ext.oauth import OAuth

from sqlalchemy.orm import aliased, contains_eager

from datetime import datetime

oauth = OAuth()


facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='233700133415330',
    consumer_secret='1d28dccf888bb41517693847b1d335d8',
    request_token_params={'scope': 'email'}
)

toolbar = DebugToolbarExtension(app)

bcrypt = Bcrypt()
        
mail = Mail(app)

class Anonymous(AnonymousUser):
    name = u"Anonymous"

login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.init_app(app)



@login_manager.user_loader
def load_user(uid):
    return Users.query.filter_by(uid=uid).first()

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            form.text.data,
            form.text2.data,
            form.longitude.data,
            form.latitude.data,
            form.date.data,
            datetime.now(),
            current_user.get_id()
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))
    comments = Comment.query.order_by(db.desc(Comment.timestamp))
    return render_template('index.html', comments=comments, form=form)


@app.route('/map')
def show_map():
    comments = Comment.query.order_by(db.asc(Comment.date))
    
    return render_template('show_map.html', comments=comments,)

@app.route('/myevents')
def my_events():
    
    comments = Comment.query.filter_by(uid = current_user.get_id()).order_by(db.asc(Comment.date))

    return render_template('my_events.html', comments=comments,)



@app.route('/view/<event_id>')
def view_event(event_id):
    entry = Comment.query.filter_by(id = event_id).first_or_404()
    return render_template('view_event.html', entry=entry,)
    
@app.route('/edit/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    form = CommentForm()
    entry = Comment.query.filter_by(id = event_id).first_or_404()
    print entry.text2
    if form.validate_on_submit():
        comment = Comment(
            form.text.data,
            form.text2.data,
            form.longitude.data,
            form.latitude.data,
            form.date.data,
            datetime.now(),
            current_user.get_id()
        )
        entry.text = form.text.data 
        entry.text2 = form.text2.data
        entry.longitude = form.longitude.data
        entry.latitude = form.latitude.data
        entry.date = form.date.data
        db.session.commit()
        return redirect(url_for('my_events'))
    else:
        form = CommentForm(obj=entry)
        form.populate_obj(entry)
    return render_template('edit_event.html', entry=entry, form=form)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
      user = Users( 
          form.username.data,
          form.password.data,
          #form.confirm.data ,
          form.email.data,
          #form.accept_tos.data,
      )
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #user = User(
            #form.username.data,
            #form.password.data,
        #)
        #db.session.add(user)
        #db.session.commit()
        admin = Users.query.filter_by(username=form.username.data).first()
        if admin:
          if admin.check_password(form.password.data):
            #userlogedin= Users.query.filter_by(uid=uid).first()(admin.username, admin.uid, admin.email)
            login_user(admin)
            flash(admin.username + ' logged in')
            return redirect(url_for('index'))
          else:
            flash('wrong pass')
            return redirect(url_for('login'))
        else:
          flash('wrong username')
          return redirect(url_for('login'))
        
    return render_template('login.html', form=form)


@app.route('/passwordreset', methods=['GET', 'POST'])
def resetpassword():
    form = PasswordResetForm()
    if form.validate_on_submit():
        if form.username.data:
          user = Users.query.filter_by(username=form.username.data).first()
        elif form.email.data:
          user = Users.query.filter_by(email=form.email.data).first()
        else:
          flash("Username or password not in system")
          
        if user:
          if user.email:
            s = URLSafeSerializer('12fe454t')
            key = s.dumps([user.username, user.email])
            #s.loads('WzEsMiwzLDRd.wSPHqC0gR7VUqivlSukJ0IeTDgo')
            
            msg = Message("Password reset", sender="info@droopia.net", recipients=[user.email])
            msg.html = "<b>testing</b> \
                        #<a href='http://127.0.0.1:5000/passwordreset/" + key + "'>http://127.0.0.1:5000/passwordreset/" + key + "</a>"

            print msg.html
            mail.send(msg)
            
            flash('Email sent to: ' + user.email)
            return redirect(url_for('resetpassword'))
          else:
            flash('No such user')
            return redirect(url_for('resetpassword'))
        else:
            flash('No such user')
            return redirect(url_for('resetpassword'))

    return render_template('reset_password.html', form=form)


@app.route('/passwordreset/<secretstring>', methods=['GET', 'POST'])
def changepassword(secretstring):
    form = PasswordChangeForm()
    if form.validate_on_submit():
      
        if form.password.data:
          s = URLSafeSerializer('12fe454t')
          uname, uemail = s.loads(secretstring)
          user = Users.query.filter_by(username=uname).first()
          db.session.add(user)
          user.pwdhash = bcrypt.generate_password_hash(form.password.data)
          db.session.commit() 
          print user.pwdhash
          flash('succsessful password reset')
          return redirect(url_for('login'))
          
        else:
            flash('Try again')
            return redirect(url_for('resetpassword'))

    return render_template('change_password.html', form=form)
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("show_map"))



#OAuth integration

@app.route('/fblogin')
def fblogin():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash('You denied the login')
        return redirect(next_url)

    session['fb_access_token'] = (resp['access_token'], '')

    me = facebook.get('/me')
    user = Users.query.filter_by(fb_id=me.data['id']).first()
    
    if user is None:
      fb_id = me.data['id']
      
      if me.data['username']:
        fb_username = me.data['username']
      else:
        fb_username = me.data['name']

      fb_email = me.data['email']

      user = Users(fb_username, 'temp',fb_email)
      user.fb_id = me.data['id']
      user.activate  = True
      user.created = datetime.utcnow()
      db.session.add(user)
      db.session.commit()
    session['user_id'] = user.uid

    flash('You are now logged in as %s' % user.username)
    return redirect(url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('fb_access_token')   