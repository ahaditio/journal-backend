from Journal.lib.mongo import mongo_conn


def command(type):
	db = mongo_conn()
	results = db.command(type)

	return results


def find_one(collection, pipeline):
	db = mongo_conn()
	results = db[collection].find_one(pipeline)

	return results


def aggregate(collection, pipeline):
	db = mongo_conn()
	results = db[collection].aggregate(pipeline, allowDiskUse=True)

	return results


def insert_many(collection, pipeline):
	try:
		db = mongo_conn()
		db[collection].insert_many(pipeline)
		return 'Success'
	except Exception as e:
		return e