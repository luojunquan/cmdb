import hashlib

def encrypt_password(password):
    if not isinstance(password, bytes):
        password = str(password).encode()

    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

print(encrypt_password(123456))