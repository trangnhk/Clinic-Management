import os
from sqlalchemy.pool import NullPool

class BaseConfig:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'NgoHoangKieuTrang'
    JWT_SECRET_KEY = 'Nhinho3008'   
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Nhinho3008@localhost/clinicdb"

class BusinessConfig():
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 5
    MAX_PER_PAGE = 20
class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Nhinho3008@localhost/clinic_testdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# class ProductionConfig(BaseConfig):
#     """Production configuration."""
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'


# def get_config_by_name(config_name):
#     """ Get config by name """
#     if config_name == 'development':
#         return DevelopmentConfig()
#     elif config_name == 'production':
#         return ProductionConfig()
#     elif config_name == 'testing':
#         return TestingConfig()
#     else:
#         return DevelopmentConfig()
