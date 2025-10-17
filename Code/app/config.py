import os
from urllib.parse import quote_plus


class Config:
    """Application configuration class"""

    # Flask Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # API Config
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:1433/')

    # Database Config
    DB_SERVER = os.getenv('DB_SERVER', 'skill.database.windows.net')
    DB_NAME = os.getenv('DB_NAME', 'skilldb')
    DB_USERNAME = os.getenv('DB_USERNAME', 'DELPHINS')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Delphin@hackathon2025')
    DB_PORT = os.getenv('DB_PORT', '1433')
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 18 for SQL Server')
    DB_CERTIFICATE_PATH = os.getenv('DB_CERTIFICATE_PATH', '/home/half/Downloads/DigiCertTLSRSA4096RootG5.crt')

    # Generate database URI
    _db_username = quote_plus(DB_USERNAME)
    _db_password = quote_plus(DB_PASSWORD)
    SQLALCHEMY_DATABASE_URI = f"mssql+pymssql://{_db_username}:{_db_password}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') == 'development'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'connect_args': {
            'timeout': 30
        }
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
