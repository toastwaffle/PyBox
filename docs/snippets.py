import hashlib


def hashfile(filepath):
    sha512 = hashlib.sha512()
    f = open(filepath, 'rb')
    try:
        sha512.update(f.read())
    finally:
        f.close()
    return sha512.hexdigest()
