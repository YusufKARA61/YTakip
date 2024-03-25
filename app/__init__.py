from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from flask_mail import Mail
from flask_migrate import Migrate  # Flask-Migrate'ı içe aktar
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os

# SQLAlchemy nesnesi oluştur
db = SQLAlchemy()

# Flask-Mail'i başlat
mail = Mail()


def create_app():
    """Flask uygulamasını yarat ve yapılandır."""
    app = Flask(__name__)

    # Uygulama konfigürasyonları
    app.config['SECRET_KEY'] = 'your_secret_key'
    default_database_url = 'postgresql://postgres:123456@localhost/dapekev2s71ha2'

    database_url = os.environ.get('DATABASE_URL', default_database_url)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'img')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'yusufkara061@gmail.com'  # Gmail adresinizi girin
    app.config['MAIL_PASSWORD'] = 'zizq lvpl lzgi dedx'  # Gmail şifrenizi girin
    app.config['MAIL_DEFAULT_SENDER'] = 'yusufkara061@gmail.com'  # Varsayılan gönderici adres
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15) # Oturumun süresini 15 dakika olarak ayarla

    # CORS'u başlat
    CORS(app)

    mail.init_app(app)

    # Flask-Principal'i başlat
    principal = Principal()

    # Flask-Principal'i app ile ilişkilendir
    principal.init_app(app)

    # CSRF korumasını başlat
    csrf = CSRFProtect(app)
    
    # Uzantıları başlat
    db.init_app(app)

    # Flask-Migrate entegrasyonunu ekleyin
    migrate = Migrate(app, db)

    # Kullanıcı modelini içe aktar
    from .models import User

    # Flask-Login'i başlat
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Kullanıcı giriş yapmadıysa yönlendirilecek sayfa
    login_manager.init_app(app)

    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Kullanıcı oturum açtığında çağrılır
        identity.user = current_user

        # Kullanıcı rollerini ekleyin
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    from .models import ModulAyar

    @app.context_processor
    def inject_modulayar():
        modulayar = ModulAyar.query.first()  # ModulAyar modelinden veri alın
        return dict(modulayar=modulayar)  # Şablonlarda kullanmak üzere sözlük olarak döndür
       

    # Blueprint'leri kaydet
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    from .routes.proje import proje as proje_blueprint
    app.register_blueprint(proje_blueprint)
    from .routes.api import api_blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    from .routes.riskli import riskli as riskli_blueprint
    app.register_blueprint(riskli_blueprint)
    from .routes.firma import firma as firma_blueprint
    app.register_blueprint(firma_blueprint)
    from .routes.ruhsat import ruhsat as ruhsat_blueprint
    app.register_blueprint(ruhsat_blueprint)



    # Hata işleyiciyi ekleyin
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('admin/forbidden.html'), 403



    return app
