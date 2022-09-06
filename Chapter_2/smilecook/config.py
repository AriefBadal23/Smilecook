class Config:
    DEBUG = True
    # Changed from plaintext to environment variables
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://arief:lyric_lice_clippers@localhost/smilecook"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # JWT key
    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'
    
    # Set the destination of the uploaded images
    UPLOADED_IMAGES_DEST = 'static/images'

    # caching related configuration
    # default = Null (no cache) 'simple' because we make use of the SimpleCache strategy
    CACHE_TYPE = 'simple'
    # default expiration time (10 min)
    CACHE_DEFAULT_TIMEOUT = 10 * 60
