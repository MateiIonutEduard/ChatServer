import os
from base64 import *
import hashlib


def getHash(key):
    buffer = hashlib.sha256(key.encode('utf-8'))
    return b64encode(buffer.digest()).decode('utf-8')


def getApiKey():
    buf = os.urandom(16)
    apiKey = b64encode(buf).decode('utf-8')
    return apiKey
