from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES
from flask_caching import Cache
# Create an uploadset named images to upload files with the type of IMAGES(.jpg, .jpeg, .png)
image_set = UploadSet('images', IMAGES)

# new instance of flask-cache 
cache = Cache()

# new db instance of SQLalchamy
db = SQLAlchemy()

# new instace of  flask-jwt-extended
jwt = JWTManager()


