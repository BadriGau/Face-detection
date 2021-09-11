import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'#\x81\xce\xb1\xdc\xc4k\x15:\x8f\xa2m\xcc\xc3V\xc1'