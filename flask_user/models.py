# -*- coding: utf-8 -*-
import datetime
from flask_user.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr


db = SQLAlchemy()


users = db.Table('users',
                 db.Column('user_id',
                           db.Integer,
                           db.ForeignKey('user.id'),
                           primary_key=True),
                 db.Column('tenant_id',
                           db.Integer,
                           db.ForeignKey('tenant.id'),
                           primary_key=True)
                 )


themes = db.Table('themes',
                  db.Column('themes_id',
                            db.Integer,
                            db.ForeignKey('theme.id'),
                            primary_key=True),
                  db.Column('tenant_id',
                            db.Integer,
                            db.ForeignKey('tenant.id'),
                            primary_key=True)
                  )


# Define the User data model. Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column(
        'is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(
        db.String(100), nullable=False, server_default='')
    last_name = db.Column(
        db.String(100), nullable=False, server_default='')


class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(200), nullable=False, unique=True)
    users = db.relationship('User', secondary=users, lazy='subquery',
                            backref=db.backref('tenants', lazy=True))
    themes = db.relationship('Theme', secondary=themes, lazy='subquery',
                             backref=db.backref('users', lazy=True))

    @classmethod
    def by_tenant(cls, dbsession, tenant_id):
        return dbsession.query(cls).filter_by(id=tenant_id).all()

    @classmethod
    def by_tenants(cls, dbsession, tenants_id):
        return dbsession.query(cls).filter(cls.id.in_(tenants_id))


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(255), nullable=False)


class TenantModel(db.Model):
    __abstract__ = True

    @declared_attr
    def theme_id(cls):
        return db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)

    @declared_attr
    def tenant_id(cls):
        return db.Column(db.Integer, db.ForeignKey('tenant.id'),
                         nullable=False)

    id = db.Column(db.Integer, primary_key=True)


class Item(TenantModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
