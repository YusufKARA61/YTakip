from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_principal import Permission, Principal, RoleNeed
from app.models import User, Ayarlar, ModulAyar, MailSettings, KdsidAyar, db, roles_users, Role, Harita, Department, SubDepartment
from app.permissions import admin_permission
from app.forms import AyarlarForm, ModulAyarForm, MailSettingsForm, KdsidAyarForm, AssignRoleForm, UserProfileForm, UserPasswordForm, AddUserForm, DepartmentForm, SubDepartmentForm, RoleForm
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
    # Departman ve alt departman seçimlerini form içine ekleyin
    form = AddUserForm()
    form.department.choices = [(d.id, d.name) for d in Department.query.all()]
    form.sub_department.choices = [(sd.id, sd.name) for sd in SubDepartment.query.all()]
    
    if form.validate_on_submit():
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
            department_id=form.department.data,
            sub_department_id=form.sub_department.data,
            membership_type=form.role.data,
            active=True,
            email_confirmed=True
        )

        # Seçilen rolü al
        selected_role = Role.query.get(form.role.data)

        # Yeni kullanıcıya rol ata
        new_user.roles.append(selected_role)

        db.session.add(new_user)
        db.session.commit()

        flash('Yeni kullanıcı başarıyla eklendi.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/add_user.html', form=form)



@admin.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        flash('Departman başarıyla eklendi.', 'success')
        return redirect(url_for('admin.add_department'))
    departments = Department.query.all()
    return render_template('admin/add_department.html', form=form, departments=departments)

@admin.route('/add_sub_department', methods=['GET', 'POST'])
def add_sub_department():
    form = SubDepartmentForm()
    if form.validate_on_submit():
        sub_department = SubDepartment(name=form.name.data, department_id=form.department_id.data)
        db.session.add(sub_department)
        db.session.commit()
        flash('Alt departman başarıyla eklendi.', 'success')
        return redirect(url_for('admin.add_sub_department'))
    sub_departments = SubDepartment.query.all()
    return render_template('admin/add_sub_department.html', form=form, sub_departments=sub_departments)

@admin.route('/add_role', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_role():
    form = RoleForm()
    if form.validate_on_submit():
        new_role = Role(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_role)
        db.session.commit()
        flash('Yeni rol başarıyla eklendi.', 'success')
        return redirect(url_for('admin.add_role'))
    return render_template('admin/add_role.html', form=form)

@admin.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Kullanıcı başarıyla silindi.', 'success')
    else:
        flash('Kullanıcı bulunamadı.', 'error')

    return redirect(url_for('admin.users'))



@admin.route('/assign_role', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def assign_role():
    form = AssignRoleForm()
    if form.validate_on_submit():
        user_id = form.user.data
        role_id = form.role.data
        user = User.query.get(user_id)
        role = Role.query.get(role_id)
        if user and role:
            # Kullanıcıya rol ekleme
            if role not in user.roles:
                user.roles.append(role)
            # Kullanıcının membership_type sütununu güncelleme
            user.membership_type = role.name
            db.session.commit()
            flash('Rol başarıyla atandı ve kullanıcı türü güncellendi.', 'success')
        else:
            flash('Kullanıcı veya rol bulunamadı.', 'error')
        return redirect(url_for('admin.assign_role'))
    return render_template('admin/assign_role.html', form=form)


@admin.route('/admin/profile', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def user_profile():
    user = current_user
    profile_form = UserProfileForm(obj=user)
    password_form = UserPasswordForm()
    
    if "profile_submit" in request.form and profile_form.validate_on_submit():
        # Profil güncelleme işlemleri
        user.first_name = profile_form.first_name.data
        user.last_name = profile_form.last_name.data
        user.email = profile_form.email.data
        # Profil resmi ve diğer alanlar için ek işlemler...
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('admin.user_profile'))

    if "password_submit" in request.form and password_form.validate_on_submit():
        # Şifre güncelleme işlemleri
        if user.check_password(password_form.current_password.data):
            user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Your password has been changed.', 'success')
        else:
            flash('Current password is not correct.', 'danger')
        return redirect(url_for('admin.user_profile'))
    
    return render_template('admin/profile.html', profile_form=profile_form, password_form=password_form)

