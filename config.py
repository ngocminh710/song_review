import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:0512@localhost:5433/Song'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ROOT_PATH = basedir
    STATIC_FOLDER = os.path.join(basedir, 'app//View//static')
    TEMPLATE_FOLDER = os.path.join(basedir, 'app//View//templates')
