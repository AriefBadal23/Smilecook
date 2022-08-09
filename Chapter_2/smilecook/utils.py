from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import uuid
from flask_uploads import extension
from extensions import image_set

def generate_token(email, salt=None):
    """ Generates a token via email for the user account  """
    # Verify the token by using the secret key (with a timestamp)
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(email, salt=salt)


def verify_token(token, max_age=(30*60), salt=None):
    """ Method which will extract the email address from the token,
        which will confirm wheter the valid period in the token is
         within 30 minutes (30*60 seconds) """
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    try:
        email = serializer.loads(token, max_age=max_age, salt=salt)
    except:
        return False
    return email


def hash_password(password):
    """ Takes care of the password hashing """
    return pbkdf2_sha256.hash(password)


def check_password(password, hashed):
    """ Used for user authentication by comparing password and hash
         in the db """
    return pbkdf2_sha256.verify(password, hashed)

def save_image(image, folder):
    # uuid is to generate the filename for the uploaded image
    filename = '{}.{}'.format(uuid.uuid4(), extension(image.filename))
    image_set.save(image, folder=folder, name=filename)
    return filename


    