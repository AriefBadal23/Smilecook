from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import uuid
from flask_uploads import extension
from extensions import image_set, cache
from PIL import Image
import os

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



def compress_image(filename, folder):
    # Get the image file's location
    file_path = image_set.path(filename=filename, folder=folder)
    # Create the image object from the image file
    image = Image.open(file_path)
    # Change the color mode to RGB
    if image.mode != "RGB":
        image.convert("RGB")
    # Resize the sides so that the image is not bigger than 1600 px
    if max(image.width, image.height) > 1600:
        maxsize=(1600,1600)
        image.thumbnail(maxsize, Image.ANTIALIAS)
    # generate the filename
    compressed_filename = '{}.jpg'.format(uuid.uuid4())
    # Set the location of the comppressed image
    compressed_file_path = image_set.path(filename=compressed_filename, folder=folder)
    # Save the compressed image                     
    # quality indicates the quality of the image which can range from 1 to 100, 1= worst and 95=best
    # optimize; attempt to compress the palette by eliminating unused colors.
    image.save(compressed_file_path, optimize=True, quality=85)

    # Get the size in bytes to get the original size for a before after comparison(testing)
    original_size = os.stat(file_path).st_size
    # os.stat returns the size of the image
    compressed_size = os.stat(compressed_file_path).st_size
    percentage = round((original_size - compressed_size) / original_size * 100)
    print("The file size is reduced by {}%, from {} to {}".format(percentage, original_size, compressed_size))

    # Remove the original image and return the compressed image filename
    os.remove(file_path)
    return compressed_filename

def save_image(image, folder):
    # uuid(Universal Unique Identifier) is to generate the filename for the uploaded image
    # getting the file extension from the uploaded image using the exension function
    filename = '{}.{}'.format(uuid.uuid4(), extension(image.filename))
    
    # Save the image in the folder
    image_set.save(image, folder=folder, name=filename)

    filename = compress_image(filename=filename, folder=folder)
    return filename

def clear_cache(key_prefix):
    # iterate all the keys in the cache if True place it in the keys list
    keys = [key for key in cache.cache._cache.keys() if key.startswith(key_prefix)]
    # clear cache (* will unpack the list with positional. arguments)
    cache.delete_many(*keys)