from pymongo import MongoClient
import json

with open('config.json') as configfile:
    config = json.load(configfile)
    mongo = config['MONGO_CONFIG']

def mongo_conn():
	hostList  = mongo['host']
	database  = mongo['database']
	temp_host = ''
	for i in hostList:
		temp_host = temp_host + i + ','
	temp_host = temp_host[:-1]
	connectTimeoutMs = mongo['timeout']
	conn_read 	= MongoClient('mongodb://'+temp_host+'/?connectTimeoutMS='+str(connectTimeoutMs))
	db 			= conn_read.Journal

	return db
