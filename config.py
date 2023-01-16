import os
class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # JWT key
    # SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'
    
    # Set the destination of the uploaded images
    UPLOADED_IMAGES_DEST = 'static/images'

    # caching related configuration
    # default = Null (no cache) 'simple' because we make use of the SimpleCache strategy
    CACHE_TYPE = 'simple'
    # default expiration time (10 min)
    CACHE_DEFAULT_TIMEOUT = 10 * 60

    # allows Flask limiter to put rate-limit-related information in the HTTP header
    # including the X-RateLimit-Limit X-RateLimit-Remaining, X-RateLimit-Reset, and Retry-After
    RATELIMIT_HEADERS_ENABLED = True


class DevelopmentConfig(Config):
    """ Classes to seperate Development and Production environments configurations """
    DEBUG = True
    SECRET_KEY = 'super-secret-key'

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATATBASE_URI')
    hostname = os.environ(os.environ['DB_HOST'])
    DB_USER = os.environ['DBUSER']
    DBNAME = os.environ['DBNAME']
    HOST = hostname + ".postgres.database.azure.com"
    PASSWORD = os.environ('DB_PASS')

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{PASSWORD}@{HOST}:5432/{DBNAME}"    


class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATATBASE_URI')
    

