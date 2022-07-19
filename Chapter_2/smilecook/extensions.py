from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# new db instance of SQLalchamy
db = SQLAlchemy()

# new instace of  flask-jwt-extended
jwt = JWTManager()
