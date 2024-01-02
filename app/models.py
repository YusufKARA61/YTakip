from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_principal import Principal, RoleNeed, Permission
from datetime import datetime
from . import db

# Ara tablo 'roles_users' için ForeignKey referansları güncellendi
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('tbl_users.user_id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'tbl_users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    membership_type = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    def get_id(self):
        return str(self.user_id)

class Ayarlar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100))
    site_title = db.Column(db.String(100))
    site_logo = db.Column(db.String(100))
    google_analytics = db.Column(db.String(100))
    site_instagram = db.Column(db.String(100))
    site_facebook = db.Column(db.String(100))
    site_twitter = db.Column(db.String(100))
    site_youtube = db.Column(db.String(100))
    seo_description = db.Column(db.String(255))
    seo_keywords = db.Column(db.String(255))

class ModulAyar(db.Model):
    __tablename__ = 'modul_ayar'
    id = db.Column(db.Integer, primary_key=True)
    kullanıcılar_aktif = db.Column(db.Boolean, default=True)
    blog_aktif = db.Column(db.Boolean, default=True)
    mesajlar_aktif = db.Column(db.Boolean, default=True)
    projeler_aktif = db.Column(db.Boolean, default=True)
    riskli_yapı_aktif = db.Column(db.Boolean, default=True)
    # Diğer modüller için benzer alanlar...

class MailSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail_server = db.Column(db.String(120))
    mail_port = db.Column(db.Integer)
    mail_use_tls = db.Column(db.Boolean)
    mail_username = db.Column(db.String(120))
    mail_password = db.Column(db.String(120))
    mail_default_sender = db.Column(db.String(120))

class Proje(db.Model):
    __tablename__ = 'tbl_projeler'
    proje_id = db.Column(db.Integer, primary_key=True)
    proje_adi = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_users.user_id'))
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    is_site = db.Column(db.Boolean, default=False)  # Yeni alan: is_site

    # User modeli ile ilişki ekleyin
    user = db.relationship('User', backref='projeler', lazy=True)

    # Proje ile ilişkili verileri almak için relationship tanımı
    veriler = db.relationship('Veri', backref='proje', lazy=True)


class Veri(db.Model):
    __tablename__ = 'tbl_veri'
    veri_id = db.Column(db.Integer, primary_key=True)
    proje_id = db.Column(db.Integer, db.ForeignKey('tbl_projeler.proje_id'))
    isim = db.Column(db.String(100))
    telefon = db.Column(db.String(15))
    tcno = db.Column(db.String(11))
    mvid = db.Column(db.Float)
    kdsid = db.Column(db.Float)
    arsaalan = db.Column(db.Float)
    kisiarsaalan = db.Column(db.Float)
    hisseoran = db.Column(db.Float)
    ada = db.Column(db.Integer)
    parsel = db.Column(db.Integer)
    onay_durumu = db.Column(db.Boolean, default=False)




