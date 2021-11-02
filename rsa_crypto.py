import rsa

def keys():
    public, private = rsa.newkeys(512)
    return public, private

def encrypt(message, public):
    return rsa.encrypt(message.encode(), public)

def decrypt(encr, private):
    return rsa.decrypt(encr, private).decode()