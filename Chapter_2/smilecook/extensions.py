from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES

image_set = UploadSet('images', IMAGES)

# new db instance of SQLalchamy
db = SQLAlchemy()

# new instace of  flask-jwt-extended
jwt = JWTManager()
