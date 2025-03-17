import os

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/boxtrack')

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL', 'postgresql://postgres:postgres@localhost:5432/boxtrack_test') 