from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_principal import Permission, RoleNeed
from app.models import User, Ayarlar, ModulAyar, MailSettings, KdsidAyar
from app.permissions import admin_permission
from app.forms import AyarlarForm, ModulAyarForm, MailSettingsForm, KdsidAyarForm
from werkzeug.utils import secure_filename
from flask import current_app
from app import db
import os

admin = Blueprint('admin', __name__)


@admin.route('/admin/dashboard')
@login_required
@admin_permission.require(http_exception=403)
def admin_dashboard():
    return render_template('admin/dashboard.html')

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




