#_*_ coding:utf-8 _*_
# Required() 忘记写括号
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email =StringField('Email',validators=[Required(),Length(1,64),Email()])

    password = PasswordField('password',validators=[Required()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log in')

class RegisterationForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username=StringField('username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                                            'usernames must have only letters,'
                                                                        'numbers,dots or underscores')])
    password =PasswordField('password',validators=[
        Required(),EqualTo('password2',message='Password must match.')])
    password2=PasswordField('Confirm password',validators=[Required()])
    submit =SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')