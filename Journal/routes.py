from flask import render_template, g, make_response, request, Flask, redirect, url_for, abort, current_app
from flask.json import jsonify
from flask_cors import CORS
from Journal import app, socketio
from Journal.account import token_handler

import json
import time

with open('config.json') as configfile:
    config = json.load(configfile)
    secretkey = config['AUTHORIZATION']['secretkey']
    algorithm = config['AUTHORIZATION']['algorithm']

from Journal.account.user import user
from Journal.lib.auth import auth

authObj = auth(secretkey, algorithm)
userObj = user(authObj)

CORS(app, resources={r"/v1/*": {"origins": "*"}}, expose_headers="Content-Disposition")

@app.before_request
def begin_request():
    print('Request Start')
    return token_handler.init(request)

@app.after_request
def after_request(response):
    print('Request End')
    return response

@app.route('/')
@app.route('/home')
def home():
    return "This is a home page that you asked for !"

@app.route('/users/login', methods=['POST'])
def user_login():
    userAuthInfo = {
        'username' : request.json['username'],
        'password' : request.json['password']
    }
    reData = userObj.user_login(userAuthInfo)
    if reData['statusCode'] == 401:
        return jsonify({'message':reData['status'], 'status': 50}), 401
    elif reData['statusCode'] == 500:
        return jsonify({'message':reData['status'], 'status': 52}), 500
    elif reData['statusCode'] == 200:
        return jsonify({'message':reData['status'], 'token':reData['token']}), 200

@app.route('/publish', methods=['POST'])
def publish():
    tes = request.args.getlist("tes")[0]

    return tes