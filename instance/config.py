import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class ProductionConfig(Config):
    """Configurations for production
    """


class StagingConfig(Config):
    """Configurations for staging
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class TestingConfig(Config):
    """Configurations for testing
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')


app_config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'testing': TestingConfig
}