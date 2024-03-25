# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, RadioField, EmailField, FileField, IntegerField, FloatField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length
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
        ('muteahhit', 'Müteahhit')
    ])
    

    
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
    mesajlar_aktif = BooleanField('Yapı Ruhsat Modülü')
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


class RiskliForm(FlaskForm):
    YKN = StringField('YKN', validators=[Optional(), Length(max=255)])
    ADI = StringField('Adı', validators=[Optional(), Length(max=255)])
    ADA = StringField('Ada', validators=[DataRequired(), Length(max=255)])
    PARSEL = StringField('Parsel', validators=[DataRequired(), Length(max=255)])
    MAHALLE = StringField('Mahalle', validators=[DataRequired(), Length(max=255)])
    CADDE = StringField('Cadde', validators=[Optional(), Length(max=255)])
    SOKAK = StringField('Sokak', validators=[Optional(), Length(max=255)])
    BINA_NO = StringField('Bina No', validators=[Optional(), Length(max=255)])
    DURUMU = StringField('Durumu', validators=[DataRequired(), Length(max=255)])
    TESISAT_KESIM_TARIHI = DateField('Tesisat Kesim Tarihi', format='%Y-%m-%d', validators=[Optional()])
    YIKIM_TARIHI = DateField('Yıkım Tarihi', format='%Y-%m-%d', validators=[Optional()])
    PERSONEL = StringField('Personel', validators=[Optional(), Length(max=255)])
    BASVURU_TARIHI = DateField('Başvuru Tarihi', format='%Y-%m-%d', validators=[Optional()])
    BASVURU_NO = StringField('Başvuru No', validators=[Optional(), Length(max=255)])
    KAT_SAYISI = IntegerField('Kat Sayısı', validators=[Optional()])
    BETON_BASINC_DAYANIMI_MPA = IntegerField('Beton Basınç Dayanımı (MPa)', validators=[Optional()])
    OZEL_NOT = TextAreaField('Özel Not', validators=[Optional()])

    submit = SubmitField('Kaydet')

class FirmaBilgileriForm(FlaskForm):
    firma_ad = StringField('Firma Adı', validators=[DataRequired(), Length(min=2, max=255)])
    vergi_no = StringField('Vergi Numarası', validators=[DataRequired(), Length(min=10, max=50)])
    yetkili_tc = StringField('Yetkili TC Kimlik Numarası', validators=[DataRequired(), Length(min=11, max=11)])
    yetkili_ad = StringField('Yetkili Adı ve Soyadı', validators=[DataRequired(), Length(min=2, max=255)])
    firma_adres = StringField('Firma Adresi', validators=[DataRequired()])
    tel_no = StringField('Telefon Numarası', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('E-Mail Adresi', validators=[DataRequired(), Email()])
    iban_no = StringField('IBAN Numarası', validators=[DataRequired(), Length(min=24, max=34)])
    mut_sinif = StringField('Muhasebe Sınıfı', validators=[DataRequired()])
    submit = SubmitField('Kaydet')

# İstanbul Bağcılar ilçesine ait mahallelerin listesi
bagcilar_mahalleleri = [
    ('0', '100. Yıl Mahallesi'),
    ('1', 'Göztepe Mahallesi'),
    ('2', 'Kazım Karabekir Mahallesi'),
    ('3', 'Fatih Mahallesi'),
    ('4', 'Çınar Mahallesi'),
    ('5', 'Demirkapı Mahallesi'),
    ('6', 'Fevzi Çakmak Mahallesi'),
    ('7', 'Güneşli Mahallesi'),
    ('8', 'Hürriyet Mahallesi'),
    ('9', 'İnönü Mahallesi'),
    ('10', 'Kemalpaşa Mahallesi'),
    ('11', 'Kirazlı Mahallesi'),
    ('12', 'Mahmutbey Mahallesi'),
    ('13', 'Barbaros Mahallesi'),
    ('14', 'Sancaktepe'),
    ('15', 'Bağlar Mahallesi'),
    ('16', '15 Temmuz Mahallesi'),
    ('17', 'Yavuz Selim Mahallesi'),
    ('18', 'Yenigün Mahallesi'),
    ('19', 'Yenimahalle'),
    ('20', 'Yıldıztepe Mahallesi'),
    ('21', 'Sancaktepe Mahallesi'),
]

class RuhsatBilgileriForm(FlaskForm):
    yapi_adi = StringField('Yapı Adı', validators=[DataRequired()])
    ruhsat_tarihi = DateField('Ruhsat Tarihi', format='%Y-%m-%d', validators=[DataRequired()])
    zabit_tarih = DateField('Zabıt Tarihi', format='%Y-%m-%d')
    imar_barisi = BooleanField('İmar Barışı')
    mahalle = SelectField('Mahalle', choices=bagcilar_mahalleleri, validators=[DataRequired()])
    ada = IntegerField('Ada', validators=[DataRequired()])
    parsel = IntegerField('Parsel', validators=[DataRequired()])
    parsel_turu = StringField('Parsel Türü')
    mevcut_insaat_alan = FloatField('Mevcut İnşaat Alanı')
    tapu_alani = FloatField('Tapu Alanı', validators=[DataRequired()])
    blok_sayi = FloatField('Blok Sayısı')
    konut_bb_sayi = FloatField('Konut Bağımsız Bölüm Sayısı', validators=[DataRequired()])
    ticari_bb_sayi = FloatField('Ticari Bağımsız Bölüm Sayısı', validators=[DataRequired()])
    toplam_bb_sayi = StringField('Toplam Bağımsız Bölüm Sayısı')  # Otomatik hesaplanacak, bu yüzden doğrulayıcı yok.
    toplam_insaat_alan = FloatField('Toplam İnşaat Alanı', validators=[DataRequired()])
    yapi_yuksekligi = FloatField('Yapı Yüksekliği (metre cinsinden)', validators=[DataRequired()])
    zemin_alti_kat_sayisi = IntegerField('Zemin Altı Kat Sayısı', validators=[DataRequired()])
    zemin_ustu_kat_sayisi = IntegerField('Zemin Üstü Kat Sayısı', validators=[DataRequired()])
    submit = SubmitField('Kaydet')
