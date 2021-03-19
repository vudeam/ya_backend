import os

basedir = os.path.abspath(os.path.dirname(__file__))

settings = {
    'host': '0.0.0.0',
    'port': 8080,
    'is_debug': True,
    'db_name': 'slasty.db',
    'test_db': 'slasty_test.db',
    'basedir': basedir
}


class Config(object):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, settings["test_db"])}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
