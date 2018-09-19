import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URI = os.getenv('DATABASE_URI')


class ProductionConfig(Config):
    """Configurations for production
    """


class StagingConfig(Config):
    """Configurations for staging
    """
    TESTING = True


class TestingConfig(Config):
    """Configurations for testing
    """
    DEBUG = True
    TESTING = True


app_config = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'testing': TestingConfig
}