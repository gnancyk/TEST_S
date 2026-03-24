class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mon_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ma_clé_secrète'


class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mon_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ma_clé_secrète'
    
    

class ProdConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mon_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ma_clé_secrète'
