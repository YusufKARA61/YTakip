from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_principal import Permission, Principal, RoleNeed
from app.models import User, Ayarlar, ModulAyar, MailSettings, KdsidAyar, db, roles_users, Role, Harita
from app.permissions import admin_permission
from app.forms import AyarlarForm, ModulAyarForm, MailSettingsForm, KdsidAyarForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import current_app
import os

admin = Blueprint('admin', __name__)

# Admin rolüne sahip kullanıcıların tüm rolleri ekleyebilmesi için izin tanımlama
admin_can_add_all_roles_permission = Permission(RoleNeed('admin_can_add_all_roles'))



@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_count = Harita.query.count()  # Toplam kayıt sayısı
    true_count = Harita.query.filter_by(kdalan=True).count()  # kdalan True olan kayıtların sayısı
    
    # Verileri şablona gönder
    return render_template('admin/dashboard.html', total_count=total_count, true_count=true_count)

@admin.route('/admin/ayarlar', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def ayarlar():
    ayar = Ayarlar.query.get(1) or Ayarlar()
    form = AyarlarForm(obj=ayar)

    if form.validate_on_submit():
        if form.site_name.data:
            ayar.site_name = form.site_name.data
        if form.site_title.data:
            ayar.site_title = form.site_title.data
        if 'site_logo' in request.files:
            file = request.files['site_logo']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                ayar.site_logo = filename
        if form.google_analytics.data:
            ayar.google_analytics = form.google_analytics.data
        if form.site_instagram.data:
            ayar.site_instagram = form.site_instagram.data
        if form.site_facebook.data:
            ayar.site_facebook = form.site_facebook.data
        if form.site_twitter.data:
            ayar.site_twitter = form.site_twitter.data
        if form.site_youtube.data:
            ayar.site_youtube = form.site_youtube.data
        if form.seo_description.data:
            ayar.seo_description = form.seo_description.data
        if form.seo_keywords.data:
            ayar.seo_keywords = form.seo_keywords.data
        
        db.session.add(ayar)
        db.session.commit()
        flash('Ayarlar güncellendi', 'success')
        return redirect(url_for('admin.ayarlar'))

    return render_template('admin/ayarlar.html', form=form, ayar=ayar)

@admin.route('/modul-ayarlari', methods=['GET', 'POST'])
def modul_ayarlari():
    modulayar = ModulAyar.query.first() or ModulAyar()
    form = ModulAyarForm(obj=modulayar)
    
    if form.validate_on_submit():
        form.populate_obj(modulayar)
        db.session.add(modulayar)
        db.session.commit()
        flash('Modül ayarları güncellendi', 'success')
        return redirect(url_for('admin.modul_ayarlari'))

    return render_template('admin/modul_ayarlari.html', form=form, modulayar=modulayar)

@admin.route('/admin/mail-settings', methods=['GET', 'POST'])
def mail_settings():
    form = MailSettingsForm()
    settings = MailSettings.query.first()

    if form.validate_on_submit():
        if not settings:
            settings = MailSettings()
            db.session.add(settings)
        
        settings.mail_server = form.mail_server.data
        settings.mail_port = form.mail_port.data
        settings.mail_use_tls = form.mail_use_tls.data
        settings.mail_username = form.mail_username.data
        settings.mail_password = form.mail_password.data
        settings.mail_default_sender = form.mail_default_sender.data

        db.session.commit()
        flash('Mail settings updated successfully.')

    elif settings:
        form.mail_server.data = settings.mail_server
        form.mail_port.data = settings.mail_port
        form.mail_use_tls.data = settings.mail_use_tls
        form.mail_username.data = settings.mail_username
        form.mail_password.data = settings.mail_password
        form.mail_default_sender.data = settings.mail_default_sender

    return render_template('admin/mail_settings.html', form=form)

@admin.route('/admin/kdsid-ayarlari', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def kdsid_ayarlari():
    ayar = KdsidAyar.query.first() or KdsidAyar()
    form = KdsidAyarForm(obj=ayar)

    if form.validate_on_submit():
        form.populate_obj(ayar)
        db.session.add(ayar)
        db.session.commit()
        flash('KDSID ayarları güncellendi', 'success')
        return redirect(url_for('admin.kdsid_ayarlari'))

    return render_template('admin/kdsid_ayarlari.html', form=form)

@admin.route('/admin/users')
@login_required
@admin_permission.require(http_exception=403)
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)



@admin.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        # E-posta adresinin zaten kayıtlı olup olmadığını kontrol edin
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Bu e-posta adresi zaten kullanılıyor.', 'error')
            return render_template('admin/add_user.html', form=form)

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            email=form.email.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            active=True,
            email_confirmed=True,
            membership_type=form.membership_type.data
        )

        role = Role.query.filter_by(name=form.membership_type.data).first()
        if role:
            new_user.roles.append(role)
        else:
            flash(f"Role '{form.membership_type.data}' not found.", 'error')
            return render_template('admin/add_user.html', form=form)

        db.session.add(new_user)
        db.session.commit()

        
        flash('Hesabınız oluşturuldu, aktivasyon yapınız!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/add_user.html', form=form)





