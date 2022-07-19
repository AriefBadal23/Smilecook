from passlib.hash import pbkdf2_sha256


def hash_password(password):
    """ Takes care of the password hashing """
    return pbkdf2_sha256.hash(password)

def check_password(password, hashed):
    """ Used for user authentication by comparing password and hash in the db """
    return pbkdf2_sha256.verify(password, hashed)
