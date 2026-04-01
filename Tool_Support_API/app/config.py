import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mon_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'ma_clé_secrète')
    DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'univers')
    DEFAULT_ALLOWED_CATALOGS = os.getenv('DEFAULT_ALLOWED_CATALOGS', 'dbo,A,T,AdventureWorks').split(',')
    BATCH_PORT = os.getenv('BATCH_PORT', '88')

class DevConfig(Config):
    pass

class ProdConfig(Config):
    pass

