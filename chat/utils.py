import os
from base64 import *
import hashlib


def getHash(str):
    buffer = hashlib.sha256(str.encode('utf-8'))
    return b64encode(buffer)


def getApiKey():
    buf = os.urandom(16)
    apiKey = b64encode(buf)
    return apiKey
