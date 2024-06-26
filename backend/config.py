import os
import binascii

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or binascii.hexlify(os.urandom(16)).decode()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or binascii.hexlify(os.urandom(16)).decode()

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://ama:amabohachu@localhost:5432/postgres"

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')