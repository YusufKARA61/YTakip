# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, RadioField, EmailField, FileField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from flask_wtf.file import FileRequired, FileAllowed
from app.models import User  # User modelinizi import ettiğinizden emin olun



class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    
    # Membership Type seçeneği
    membership_type = RadioField('Üyelik Tipi', choices=[
        ('admin', 'Admin'),
        ('sef', 'Şef'),
        ('raportor', 'Raportör'),
        ('koordinator', 'Koordinatör')
    ])
    # Kullanıcı sözleşmesini kabul etme checkbox'ı
    accept_terms = BooleanField('Kullanıcı Sözleşmesini Okudum ve Kabul Ediyorum', validators=[DataRequired()])

    
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    first_name = StringField('Ad', validators=[DataRequired()])
    last_name = StringField('Soyad', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Cep Telefonu', validators=[Optional()])
    address = StringField('Adres', validators=[Optional()])
    password = PasswordField('Yeni Şifre', validators=[Optional(), EqualTo('confirm_password', message='Şifreler eşleşmeli')])
    confirm_password = PasswordField('Şifreyi Onayla')
    submit = SubmitField('Güncelle')


class AyarlarForm(FlaskForm):
    site_name = StringField('Site Adı', validators=[Optional()])
    site_title = StringField('Site Başlığı', validators=[Optional()])
    site_logo = FileField('Site Logosu')
    google_analytics = StringField('Google Analytics', validators=[Optional()])
    site_instagram = StringField('Instagram', validators=[Optional()])
    site_facebook = StringField('Facebook', validators=[Optional()])
    site_twitter = StringField('Twitter', validators=[Optional()])
    site_youtube = StringField('YouTube', validators=[Optional()])
    seo_description = StringField('SEO Açıklaması', validators=[Optional()])
    seo_keywords = StringField('SEO Anahtar Kelimeleri', validators=[Optional()])

class ModulAyarForm(FlaskForm):
    kullanıcılar_aktif = BooleanField('Kullanıcılar Modülü')
    blog_aktif = BooleanField('Blog Modülü')
    mesajlar_aktif = BooleanField('Mesajlar Modülü')
    projeler_aktif = BooleanField('Projeler Modülü')
    riskli_yapı_aktif = BooleanField('Riskli Yapı Modülü')
    # Diğer modüller için benzer alanlar...
    submit = SubmitField('Ayarları Kaydet')

class MailSettingsForm(FlaskForm):
    mail_server = StringField('Mail Server')
    mail_port = IntegerField('Mail Port')
    mail_use_tls = BooleanField('Use TLS')
    mail_username = StringField('Mail Username')
    mail_password = StringField('Mail Password')
    mail_default_sender = StringField('Default Sender')
    submit = SubmitField('Save')

class ProjeForm(FlaskForm):
    proje_adi = StringField('Proje Adı', validators=[DataRequired()])
    excel_file = FileField('Excel Dosyası', validators=[
        FileRequired(),
        FileAllowed(['xlsx'], 'Sadece Excel dosyaları!')
    ])
    koordinator_sec = SelectField('Koordinatör Seç', coerce=int)
    bose_parsel_numaralari = StringField('Var ise Boş Parsel Numaraları', description='Boş parselleri virgül ile ayırarak girin. Örnek: 2365/8,2366/12', validators=[Optional()])
    is_site = BooleanField('Site Mi?', default=False, description='Site durumu için işaretle')

    def __init__(self, *args, **kwargs):
        super(ProjeForm, self).__init__(*args, **kwargs)
        self.koordinator_sec.choices = self.get_koordinator_choices()

    @staticmethod
    def get_koordinator_choices():
        koordinatorler = User.query.filter_by(membership_type='koordinator').all()
        choices = [(koordinator.user_id, f"{koordinator.first_name} {koordinator.last_name}") for koordinator in koordinatorler]
        return choices

    submit = SubmitField('Proje Ekle')

class KdsidAyarForm(FlaskForm):
    birlesik_parsel_sayisi = IntegerField('Birleşik Parsel Sayısı', validators=[DataRequired()])
    toplam_arsa_alani_min = IntegerField('Minimum Toplam Arsa Alanı', validators=[DataRequired()])
    is_site_artis_orani = FloatField('Site Artış Oranı', validators=[DataRequired()])
    bos_parsel_artis_orani = FloatField('Boş Parsel Artış Oranı', validators=[DataRequired()])
    diger_parsel_artis_orani = FloatField('Diğer Parsel Artış Oranı', validators=[DataRequired()])
    arsa_alani_3000_artis_orani = FloatField('3000 m² Üzeri Arsa Artış Oranı', validators=[DataRequired()])
    arsa_alani_2000_artis_orani = FloatField('2000 m² Üzeri Arsa Artış Oranı', validators=[DataRequired()])
    arsa_alani_1000_artis_orani = FloatField('1000 m² Üzeri Arsa Artış Oranı', validators=[DataRequired()])
    arsa_alani_750_artis_orani = FloatField('750 m² Üzeri Arsa Artış Oranı', validators=[DataRequired()])
    arsa_alani_500_artis_orani = FloatField('500 m² Üzeri Arsa Artış Oranı', validators=[DataRequired()])
    # Gerekiyorsa diğer alanlar...
    submit = SubmitField('Ayarları Güncelle')


class SorguForm(FlaskForm):
    tcno = StringField('TC Kimlik Numarası', validators=[DataRequired()])
    submit = SubmitField('Sorgula')


