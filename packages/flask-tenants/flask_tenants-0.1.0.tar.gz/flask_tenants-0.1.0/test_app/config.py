# test_app/config.py
class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
