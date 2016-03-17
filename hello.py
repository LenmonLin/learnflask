#_*_ coding:utf-8 _*_

import os
#import MySQLdb
from flask import Flask,render_template,url_for,session,redirect,flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from  wtforms.validators  import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager

# 1,要添加extend bootstrap 模板，要导入Bootstrap才可以
# 2,404中视图函数忘记加return
# 3,使用图片，要在user.html 中添加<img src=“{{img}}”>才可以用
# 4,表单的使用，要设置app.config['SECRET_KEY]的值，才能使用，否则会报错。
# 5,app.config['SQLALCHEMY_DATABASE_URI']写成 ['SQLALCHEMY_DATABASE_URL']查到快挂了才查出来,不是URL，不要想当然，看来得多用TABLE，不要相信自己的拼写能力！

#basedir =os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/text1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    user = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role {}> '.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class NameForm(Form):
    name=StringField('What is your name ?',validators=[Required()])
    submit =SubmitField('submit')



@app.route('/',methods=['GET','POST'])
def index():
    myform = NameForm()
    if myform.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != myform.name.data:
            flash('looks like you have changed your name !')
        session['name']= myform.name.data
        return redirect(url_for('index'))
    return render_template('formindex.html',form=myform,name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    img = url_for('static',filename='cal.jpg')
    return render_template('user.html',name = name,img=img,current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404  #2,

if __name__ == '__main__':
    db.create_all()
    manager.run()