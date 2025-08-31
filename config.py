import os

class Config:
    SECRET_KEY = 'chave-secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///loja.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
