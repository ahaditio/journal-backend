from Journal.lib.mongo_handler import *

import bcrypt
import hashlib
import json

with open('config.json') as configfile:
    config = json.load(configfile)
    salt = config['AUTHORIZATION']['salt']

class user(object):
    def __init__(self, authObj):
        self.authObj = authObj
    def user_login(self, userAuthInfo = {}):
        pipeline = {
            'username' : userAuthInfo['username']
        }
        userData = find_one('account', pipeline)
        if userData == None:
            return {'statusCode' : 401, 'status': 'Username or Password is not match'}
        else:
            if userData['status'] == 0:
                return {'statusCode' : 401, 'status': 'User does not exist or deactivated. Please contact support for further information.'}
            else:
                encodedPassword = userAuthInfo['password'].encode('utf8')
                hashed = bcrypt.checkpw(encodedPassword, bcrypt.hashpw(str(userData['password']).encode('utf-8'), bcrypt.gensalt()))
                if hashed is False:
                    return {'statusCode' : 401, 'status': 'Username or Password is not match'}
                else:
                    payload = {
                        'userID' : str(userData['_id']),
                        'username' : userAuthInfo['username'],
                        'role' : userData['role']
                    }
                    userToken = self.authObj.encode(payload)
                    return {'statusCode' : 200, 'status': 'Success', 'token':str(userToken['token'])}
