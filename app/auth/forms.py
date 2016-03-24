# Required() 忘记写括号
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email

class LoginForm(Form):
    email =StringField('Email',validators=[Required(),Length(1,64),Email()])

    password = PasswordField('password',validators=[Required()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log in')
