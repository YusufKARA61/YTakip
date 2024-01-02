from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db, roles_users, Role
from app.forms import RegistrationForm, LoginForm, ProfileForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app
from app import mail


auth = Blueprint('auth', __name__)



def send_activation_email(user_email, token):
    msg = Message('Hesap Aktivasyonu', recipients=[user_email])
    msg.body = f"Lütfen hesabınızı aktive etmek için aşağıdaki linke tıklayın: {url_for('auth.activate_account', token=token, _external=True)}"
    mail.send(msg)

# Her istekten önce çalışacak fonksiyon
@auth.before_app_request
def check_user_logged_in():
    # Giriş yapmış kullanıcıların yönlendirileceği rotalar
    restricted_routes = ['auth.login', 'auth.register']

    # Kullanıcı giriş yapmışsa ve istenen rota kısıtlanmış rotalarsa, profile sayfasına yönlendir
    if current_user.is_authenticated and request.endpoint in restricted_routes:
        return redirect(url_for('auth.profile'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # E-posta adresinin zaten kayıtlı olup olmadığını kontrol edin
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Bu e-posta adresi zaten kullanılıyor.', 'error')
            return render_template('frontend/register.html', form=form)

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            email=form.email.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            active=True,
            email_confirmed=False,
            membership_type=form.membership_type.data
        )

        role = Role.query.filter_by(name=form.membership_type.data).first()
        if role:
            new_user.roles.append(role)
        else:
            flash(f"Role '{form.membership_type.data}' not found.", 'error')
            return render_template('frontend/register.html', form=form)

        db.session.add(new_user)
        db.session.commit()

        # Token oluştur ve e-posta gönder
        # Token üreteci oluşturma
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(new_user.email, salt='email-activation')
        send_activation_email(new_user.email, token)

        flash('Hesabınız oluşturuldu, aktivasyon yapınız!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('frontend/register.html', form=form)


@auth.route('/activate/<token>')
def activate_account(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-activation', max_age=3600)
    except (SignatureExpired, BadSignature):
        return 'Aktivasyon linki geçersiz veya süresi dolmuş.'

    user = User.query.filter_by(email=email).first_or_404()
    if not user.email_confirmed:
        user.email_confirmed = True
        db.session.commit()
    return redirect(url_for('main.home'))



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.email_confirmed:
                login_user(user)

                # Kullanıcının kimliğini ve rollerini güncelleyin
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.user_id))

                # Admin kontrolü
                if Role.query.filter_by(name='admin').first() in user.roles:
                    flash('Admin Dashboard\'a yönlendiriliyorsunuz.', 'success')
                    return redirect(url_for('admin.admin_dashboard'))  # Admin paneline yönlendir

                flash('You have been logged in!', 'success')
                return redirect(url_for('main.home'))  # Ana sayfaya yönlendir
            else:
                flash('Hesabınız aktive edilmemiş. Lütfen e-postanızı kontrol edin ve aktivasyon bağlantısına tıklayın.', 'warning')
        else:
            flash('Invalid email or password.', 'error')
    return render_template('frontend/login.html', form=form)

@auth.route('/profile')
@login_required
def profile():
    return render_template('frontend/profile.html', current_user=current_user)

@auth.route('/profile_ayar', methods=['GET', 'POST'])
@login_required
def profile_ayar():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data

        # Şifre değişikliği isteğe bağlı
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)

        db.session.commit()
        flash('Profiliniz güncellendi.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('frontend/profile_ayar.html', form=form)


# Kullanıcı çıkış işlemi
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
