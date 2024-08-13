import hashlib


# hashes a string and returns it
def hashes_password(password):
    password_bytes = password.encode('utf-8')

    hash_object = hashlib.sha256(password_bytes)

    hash_result = hash_object.hexdigest()

    return hash_result
