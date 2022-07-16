class Config:
    DEBUG=True
    SQLALCHEMY_DATABASE_URI= "postgresql+psycopg2://arief:lyric_lice_clippers@localhost/smilecook"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
    # JWT key
    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY='message'
    