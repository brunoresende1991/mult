#!/usr/bin/env python
from flask_script import Shell, Manager, Server

from apps.multitenant_app import app
from flask_user import models
from flask_user.models import db


def _make_context():
    return dict(app=app, db=db, models=models)

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
