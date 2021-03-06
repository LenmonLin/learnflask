#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role,Post,Permission,Follow, Comment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,Post=Post,Permission=Permission,Follow=Follow, Comment=Comment)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def initdata():
    """ cretat a new data"""
    db.create_all()
    admin_role =Role(name = 'Administrator')
    mod_role = Role(name = 'Moderator')
    user_role =Role(name = 'User')
    user_john = User(username = 'john',role=admin_role,confirmed=True,email='123@qq.com',password='123')
    user_susan = User(username = 'susan',role= user_role,confirmed=True,email='456@qq.com',password='456')
    user_david = User(username = 'david',role = user_role,confirmed=True,email='789@qq.com',password='789')
    db.session.add_all([admin_role,mod_role,user_role,user_john,user_susan,user_david])
    db.session.commit()
    Role.insert_roles()
    User.generate_fake(100)
    Post.generate_fake(100)

@manager.command
def drop():
    """
    drop the database
    """
    db.drop_all()
@manager.command
def init2():
    """
    create a text data
    """
    u =User(email='hi@example',username='hello',password='hi')
    db.session.add(u)
    db.session.commit()

@manager.command
def generate_fake():
    """
    create a fake data
    """
    User.generate_fake(100)
    Post.generate_fake(100)

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # create self-follows for all users
    User.add_self_follows()



if __name__ == '__main__':

    manager.run()
