# -*- coding: utf-8 -*-
import os
import click
from flask import Flask, render_template, send_from_directory, request
from flask import redirect, url_for
from flask_cli import FlaskCLI
from flask_login import current_user
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user.db_adapters import SQLAlchemyAdapter
from flask_user.managers import login_required, UserManager
from flask_user.models import db, User, Tenant, Theme
from flask_user.signals import user_logged_in
from sqlalchemy.orm import exc


# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///multitenant_app.sqlite')
    CSRF_ENABLED = True

    # Flask-Mail settings
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'multflask@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'tg2018.1')
    MAIL_DEFAULT_SENDER = os.getenv(
        'MAIL_DEFAULT_SENDER', 'multflask@gmail.com')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

    # Flask-User settings
    USER_APP_NAME = "MulT"                # Used by email templates


def create_app():
    """ Flask application factory """

    # Setup Flask app and app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize Flask extensions
    db.app = app
    db.init_app(app)
    mail = Mail(app)                         # Initialize Flask-Mail

    # Create all database tables
    db.create_all()

    @app.context_processor
    def subdomain():
        return {
            'subdomain': request.subdomain
        }

    @app.context_processor
    def tenant():
        return {
            'tenant': request.tenant
        }

    @app.context_processor
    def theme():
        return {
            'theme': request.tenant.themes[0] if request.tenant and
            len(request.tenant.themes) > 0 else None
        }

    @app.before_request
    def middleware_subdomain():
        domain = request.environ['HTTP_HOST']
        parts = domain.split('.')
        try:
            request.subdomain = parts[-2]
        except IndexError:
            request.subdomain = None

    @app.before_request
    def middleware_tenant():
        tenant_model = Tenant
        try:
            tenant = tenant_model.query.filter_by(
                alias=request.subdomain).one()
        except exc.NoResultFound:
            tenant = None
        request.tenant = tenant

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User, Tenant=Tenant, Theme=Theme)  # Register the User and Tenant models # noqa
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

    def theme_assign():
        try:
            tema = current_user.tenants[0].themes[0]
            if tema:
                filename_css = tema.style + '.css'
                return filename_css
            else:
                return None
        except IndexError:
            return None

    @app.route('/static/<filename>')
    def serve_static(filename):
        css_dir = os.path.join(os.getcwd(), 'flask_user', 'static')
        return send_from_directory(css_dir, filename)

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template('home.html')

    # The Members page is only accessible to authenticated users
    @app.route('/members')
    @login_required                 # Use of @login_required decorator
    def members_page():
        filename_css = theme_assign()
        if not filename_css:
            filename_css = 'default.css'
        serve_static(filename_css)
        return render_template(
            'member_page.html',
            filename=filename_css
        )
    return app


def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)
SQLAlchemy.get_model = get_model

# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

app = create_app()
FlaskCLI(app)
