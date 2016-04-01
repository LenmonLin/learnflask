#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role,Post,Permission
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,Post=Post,Permission=Permission)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def initdata():
    """ cretat a new data"""
    db.create_all()
    admin_role =Role(name = 'Admin')
    mod_role = Role(name = 'Moderator')
    user_role =Role(name = 'User')
    user_john = User(username = 'john',role=admin_role)
    user_susan = User(username = 'susan',role= user_role)
    user_david = User(username = 'david',role = user_role)
    db.session.add_all([admin_role,mod_role,user_role,user_john,user_susan,user_david])
    db.session.commit()
    Role.insert_roles()

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
if __name__ == '__main__':

    manager.run()
