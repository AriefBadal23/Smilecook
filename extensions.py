from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# Create an uploadset named images to upload files with the type of IMAGES(.jpg, .jpeg, .png)
image_set = UploadSet('images', IMAGES)

# new instance of flask-cache 
cache = Cache()

# new db instance of SQLalchamy
db = SQLAlchemy()

# new instace of  flask-jwt-extended
jwt = JWTManager()

limiter = Limiter(key_func=get_remote_address) # returns the ip-address for the current request



