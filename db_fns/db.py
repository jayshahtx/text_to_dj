import os
import sys
import pymongo
from pymongo import MongoClient


def get_auth_token():
	"""Reads in auth token from mongo_db"""
	collection = get_mongo_collection()
	return collection.find_one({'key_type' : 'access_token'})['key']

def get_refresh_token():
	"""Reads in refresh token from mongo db"""
	collection = get_mongo_collection()
	return collection.find_one({'key_type' : 'refresh_token'})['key']

def get_mongo_collection():
	"""Returns mongo collection where our auth tokens are stored"""

	MONGO_URL = os.environ.get('MONGOHQ_URL')
	DB_NAME = os.environ.get('MONGO_DB_NAME')
	DB_COLLECTION = os.environ.get('MONGO_COLLECTION_NAME')
	print MONGO_URL, DB_NAME, DB_COLLECTION
	return MongoClient(MONGO_URL)[DB_NAME][DB_COLLECTION]
	
def write_to_mongo(object_type, val):
	"""Updates the object_type if it exists with val, otherwise makes
	a new entry into db"""
	
	# get the collection
	collection = get_mongo_collection()
	
	# update/insert relevant documents
	return collection.update(
		{ 'key_type': object_type},
		{
			'key_type': object_type,
			'key': val
		},
		upsert=True
	)