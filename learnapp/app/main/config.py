import os

basedir = os.path.abspath(os.path.dirname(__file__))

# If we are using the secret key
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False

# Use this config for development
class DevelopmentConfig(Config):
    # Development config for
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', '..','..','src' 'data','flights.csv')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Use this config for Testing
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data','flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig
)

key = Config.SECRET_KEY