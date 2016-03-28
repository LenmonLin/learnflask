from flask import render_template,redirect,request,url_for,flash
from  . import  auth
from  flask.ext.login import login_required,login_user,logout_user,current_user
from .forms import LoginForm,RegisterationForm
from ..models import User
from .. import db
from ..email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):

            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html',form=form)


@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,
                  username=form.username.data,
                  password =form.password.data)
        db.session.add(user)
        db.session.commit()
        token =user.generate_confirmation_token()
        send_email(user.email,'Confirm you account','auth/email/confirm',user=user,token=token)
        flash('A confirmatino email has been sent to you by email')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    print 'a'
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('you have confirmed you accout.')
    else:
        flash('the confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated\
            and not current_user.confirmed\
            and request.endpoint[:5] !='auth.'\
            and request.endpoint !='static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'confirm your account',
               'auth/email/confirm',user=current_user,token=token)
    flash('a new confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))