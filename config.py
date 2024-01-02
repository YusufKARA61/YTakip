class Config(object):
    """
    Genel konfigürasyonlar
    """
    SECRET_KEY = 'bu_bir_gizli_anahtar'  # Örnek bir gizli anahtar
    # Diğer genel konfigürasyonlar buraya eklenebilir

class DevelopmentConfig(Config):
    """
    Geliştirme ortamı konfigürasyonları
    """
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'takip'
    MYSQL_CURSORCLASS = 'DictCursor'
    # Geliştirme ortamına özgü diğer konfigürasyonlar

class TestingConfig(Config):
    """
    Test ortamı konfigürasyonları
    """
    TESTING = True
    # Test ortamına özgü konfigürasyonlar

class ProductionConfig(Config):
    """
    Prodüksiyon ortamı konfigürasyonları
    """
    DEBUG = False
    # Prodüksiyon ortamına özgü konfigürasyonlar
    # Örneğin, gerçek veritabanı bilgileri

# Uygulamanızın varsayılan konfigürasyonunu burada belirleyebilirsiniz
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
