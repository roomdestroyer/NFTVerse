import os


basedir = os.path.abspath(os.path.dirname(__file__))
urlpath = None

ADMIN_ADDRESS = "0x68e9F0c38e31b5D4D25AbEfEE28938Ac263205a5"
CONVERSION_RATE = 73000000
# Connection_CONFIG = 'mysql+pymysql://root:1234@127.0.0.1:3308/db'
Connection_CONFIG = 'mysql+pymysql://root:1234@101.42.117.143:3306/db'


class BaseConfig:
    """app base config"""

    def __init__(self):
        pass

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '1761806916@qq.com'
    MAIL_PASSWORD = 'guwugfjglmkndgaa'
    MAIL_DEFAULT_SENDER = '1761806916@qq.com'
    WTF_CSRF_CHECK_DEFAULT = False
    CORS_HEADERS = 'Content-Type'
    SECRET_KEY = 'TPmi4aLWRbyVq8zu9v82dWYW1'
    SQLALCHEMY_DATABASE_URI = Connection_CONFIG
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    # gthqpjsfvdteegaa


class DevelopmentCofig(BaseConfig):
    def __init__(self):
        pass

    DEBUG = True


class TestingConfig(BaseConfig):
    def __init__(self):
        pass

    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    def __init__(self):
        pass

    TESTING = True
    WTF_CSRF_ENABLED = False


config = {
    'default': DevelopmentCofig,
    'development': DevelopmentCofig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

os.environ['FLASK_ENV'] = 'development'
