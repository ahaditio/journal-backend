from Journal.lib.mongo_handler import *
from Journal.lib.auth import auth
from flask import request, g, Flask
from flask.json import jsonify
from bson.objectid import ObjectId
import json
import sys, os
import requests
import time

authObj 	= auth('secretkey', algorithm = 'HS512')
tokenDecode = False

app 		= Flask(__name__)

with open('middleware_rule.json') as rule:
	rule = json.load(rule)
	bypass = rule['bypass']

# endpoint_exception = ['user_login', 'home', 'export', 'track_vid', 'get_nat_campaign_report', 'get_nat_advertising', 'get_nat_adv_chart', 'get_nat_audience', 'get_nat_video', 'get_nat_video_chart']

def __ExceptionHandler(e=''):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(exc_type, fname, exc_tb.tb_lineno, e)

def init(request = False):
	get_db_status()
	if request.method == 'OPTIONS':
		return jsonify({'message' : '', 'status' : 51}), 200
	else:
		try:
			if request.endpoint not in bypass:
				token 		= request.headers['Authorization']
				token 		= token.split(" ")[1]

				tokenDecode = authObj.decode(token)

				app.token 	= tokenDecode
				
				if tokenDecode is False:
					return jsonify({'message' : 'Session is expired', 'status' : 50}), 401
				else:
					app.token 	= tokenDecode
					result 		= find_one('account', {'_id' : ObjectId(tokenDecode['userID'])})
					if result['status'] != 1:
						return jsonify({'message': 'User Inactive, please contact administrator', 'status': 52}), 401
					else:
						app.user_data = result 

					g.token 	= token
					g.decoded 	= tokenDecode

		except Exception as e:
			print str(e)
			return jsonify({'message': 'Session is expired', 'status': 50}), 401

def get_user():
	try:
		user 	= app.token
		result 	= app.user_data

		return {
			'username' 	: user['username'],
			'user_id' 	: user['userID'],
			'role' 		: user['role'],
			'firstname' : result['firstname'],
			'lastname' 	: result['lastname'],
			'status'	: result['status'],
			'idsite'	: result['idsite'],
		}

	except Exception as e:
		__ExceptionHandler(e)

def get_db_status():
	# 
	print "======= DB Server Mongo Status ========"
	serverStatus = command('serverStatus')
	print 'current 	: ' + str(serverStatus['connections']['current'])
	print 'available 	: ' + str(serverStatus['connections']['available'])
	print "================================="



	