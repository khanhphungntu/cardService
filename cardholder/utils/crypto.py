from cryptography.fernet import Fernet
import json
from django.conf import settings
import random
import string

def encrypt(cardInfo: dict):
    cardString = json.dumps(cardInfo).encode('utf-8')
    cipher = Fernet(settings.PRIVATE_KEY)
    return cipher.encrypt(cardString).decode('utf-8')

def decrypt(encryptStr: str):
    cipher = Fernet(settings.PRIVATE_KEY)
    data = cipher.decrypt(encryptStr.encode('utf-8'))
    cardInfo = json.loads(data.decode('utf-8'))
    return cardInfo

def publicKeyGenerator():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(32))

def privateKeyGenerator():
    byteKey = Fernet.generate_key()
    key = byteKey.decode('utf-8')
    return str(key)

def randomStr(length: int):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))