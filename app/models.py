from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
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
    def has_role(self, role_name):
        """Belirtilen role sahip olup olmadığını kontrol eder."""
        return any(role.name == role_name for role in self.roles)

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

class KdsidAyar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birlesik_parsel_sayisi = db.Column(db.Integer, nullable=False)
    toplam_arsa_alani_min = db.Column(db.Integer, nullable=False)
    is_site_artis_orani = db.Column(db.Float, nullable=False)
    bos_parsel_artis_orani = db.Column(db.Float, nullable=False)
    diger_parsel_artis_orani = db.Column(db.Float, nullable=False)
    arsa_alani_3000_artis_orani = db.Column(db.Float, nullable=False)
    arsa_alani_2000_artis_orani = db.Column(db.Float, nullable=False)
    arsa_alani_1000_artis_orani = db.Column(db.Float, nullable=False)
    arsa_alani_750_artis_orani = db.Column(db.Float, nullable=False)
    arsa_alani_500_artis_orani = db.Column(db.Float, nullable=False)
    # Gerekiyorsa diğer alanlar...

class Harita(db.Model):
    __tablename__ = 'harita'
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry('MULTIPOLYGON'), nullable=True)
    oda_id = db.Column(db.BigInteger, nullable=True)
    geom_type = db.Column(db.BigInteger, nullable=True)
    line_thickness = db.Column(db.BigInteger, nullable=True)
    line_type = db.Column(db.BigInteger, nullable=True)
    color_code = db.Column(db.BigInteger, nullable=True)
    thickness = db.Column(db.BigInteger, nullable=True)
    factor = db.Column(db.BigInteger, nullable=True)
    text_data = db.Column(db.String, nullable=True)
    object_properties = db.Column(db.String, nullable=True)
    point_height = db.Column(db.Float, nullable=True)
    length = db.Column(db.Float, nullable=True)
    ybizden = db.Column(db.String, nullable=True)
    ortahasar = db.Column(db.String, nullable=True)
    kdalan = db.Column(db.Boolean, default=False, nullable=False)
    riskli = db.Column(db.Boolean, default=False, nullable=False)

class Riskli(db.Model):
    __tablename__ = 'tbl_riskli'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    YKN = db.Column(db.String(255))
    ADI = db.Column(db.String(255))
    ADA = db.Column(db.String(255))
    PARSEL = db.Column(db.String(255))
    MAHALLE = db.Column(db.String(255))
    CADDE = db.Column(db.String(255))
    SOKAK = db.Column(db.String(255))
    BINA_NO = db.Column(db.String(255))
    DURUMU = db.Column(db.String(255))
    TESISAT_KESIM_TARIHI = db.Column(db.Date)
    YIKIM_TARIHI = db.Column(db.Date)
    PERSONEL = db.Column(db.String(255))
    BASVURU_TARIHI = db.Column(db.Date)
    BASVURU_NO = db.Column(db.String(255))
    KAT_SAYISI = db.Column(db.Integer)
    BETON_BASINC_DAYANIMI_MPA = db.Column(db.Integer)
    OZEL_NOT = db.Column(db.Text)


class FirmaBilgileri(db.Model):
    __tablename__ = 'firma_bilgileri'
    id = db.Column(db.Integer, primary_key=True)
    firma_ad = db.Column(db.String(255), unique=True)
    vergi_no = db.Column(db.String(50))
    yetkili_tc = db.Column(db.String(20))
    yetkili_ad = db.Column(db.String(255))
    firma_adres = db.Column(db.String(255))
    tel_no = db.Column(db.String(20))
    email = db.Column(db.String(255))
    iban_no = db.Column(db.String(34))
    mut_sinif = db.Column(db.String(50))
    referanslar = db.relationship('ReferansProje', backref='firma', lazy=True)

class ReferansProje(db.Model):
    __tablename__ = 'referans_projeler'
    id = db.Column(db.Integer, primary_key=True)
    proje_adi = db.Column(db.String(255))
    proje_resimleri = db.Column(db.Text) # JSON olarak saklanabilir
    proje_detaylari = db.Column(db.Text)
    toplam_insaat_alani = db.Column(db.Integer)
    bagimsiz_bolum_sayisi = db.Column(db.Integer)
    firma_id = db.Column(db.Integer, db.ForeignKey('firma_bilgileri.id'))

class RuhsatBilgileri(db.Model):
    __tablename__ = 'tbl_ruhsat'
    id = db.Column(db.Integer, primary_key=True)
    yapi_adi = db.Column(db.String(255))
    ruhsat_tarihi = db.Column(db.Date)
    zabit_tarih = db.Column(db.Date)
    imar_barisi = db.Column(db.Boolean)
    mahalle = db.Column(db.String(255))
    ada = db.Column(db.Integer)
    parsel = db.Column(db.Integer)
    parsel_turu = db.Column(db.String(50))
    mevcut_insaat_alan = db.Column(db.Float)
    tapu_alani = db.Column(db.Float)
    blok_sayi = db.Column(db.Integer)
    konut_bb_sayi = db.Column(db.Integer)
    ticari_bb_sayi = db.Column(db.Integer)
    toplam_bb_sayi = db.Column(db.Integer)
    toplam_insaat_alan = db.Column(db.Float)



