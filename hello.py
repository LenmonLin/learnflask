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
from flask.ext.script import Shell
from flask.ext.migrate import Migrate,MigrateCommand
# 1,要添加extend bootstrap 模板，要导入Bootstrap才可以
# 2,404中视图函数忘记加return
# 3,使用图片，要在user.html 中添加<img src=“{{img}}”>才可以用
# 4,表单的使用，要设置app.config['SECRET_KEY]的值，才能使用，否则会报错。
# 5,app.config['SQLALCHEMY_DATABASE_URI']写成 ['SQLALCHEMY_DATABASE_URL']查到快挂了才查出来,不是URL，不要想当然，看来得多用TABLE，不要相信自己的拼写能力！
# 6,session['known']拼写成【‘knowm']，这中字符串拼写错误，pycharm检查不出来，而且查错太难了，细心细心细心！！！
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
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

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
        user = User.query.filter_by(username=myform.name.data).first()

        if user is None:
            user = User(username=myform.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name']= myform.name.data
        myform.name.data = ''
        return redirect(url_for('index'))
    return render_template('formindex.html',form=myform,name=session.get('name'),known=session.get('known',False))

@app.route('/user/<name>')
def user(name):
    img = url_for('static',filename='cal.jpg')
    return render_template('user.html',name = name,img=img,current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404  #2,


def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))



if __name__ == '__main__':
    db.create_all()
    # admin_role =Role(name = 'Admin')
    # mod_role = Role(name = 'Moderator')
    # user_role =Role(name = 'User')
    # user_john = User(username = 'john',role=admin_role)
    # user_susan = User(username = 'susan',role= user_role)
    # user_david = User(username = 'david',role = user_role)
    # db.session.add_all([admin_role,mod_role,user_role,user_john,user_susan,user_david])
    # db.session.commit()
    manager.run()