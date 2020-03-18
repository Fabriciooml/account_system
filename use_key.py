from cryptography.fernet import Fernet

global f
global key
file = open('key.key', 'rb')
key = file.read()
file.close()
f = Fernet(key)

def encrypt(password):
  password = password.encode()
  encrypted = f.encrypt(password)
  return encrypted

def decrypt(encrypted):
  encrypted = encrypted.encode()
  decrypted = f.decrypt(encrypted)
  X = decrypted.decode("utf-8")
  return X