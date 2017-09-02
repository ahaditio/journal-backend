import datetime
import jwt
import hashlib
import json

with open('config.json') as configfile:
    config = json.load(configfile)
    salt = config['AUTHORIZATION']['salt']

class auth(object):
    def __init__(self, secretKey = '', algorithm = ''):
        self.secretKey = hashlib.sha224(secretKey+salt).hexdigest()
        self.algorithm = algorithm

    def encode(self, payload = {}):
        try:
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=30)
            payload['iat'] = datetime.datetime.utcnow()
            encodedToken = jwt.encode(payload, self.secretKey, algorithm=self.algorithm)
            return {'token':encodedToken}
        except:
            return {'status':'error'}

    def decode(self, token):
        try:
            decodedToken = jwt.decode(token, self.secretKey, verify=True, algorithms=self.algorithm)
            return decodedToken
        except:
            return False
