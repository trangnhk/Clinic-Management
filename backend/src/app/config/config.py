class BaseConfig:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'NgoHoangKieuTrang'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Nhinho3008@localhost/clinicdb"

# class TestingConfig(BaseConfig):
#     """Testing configuration."""
#     DEBUG = True
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'

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
