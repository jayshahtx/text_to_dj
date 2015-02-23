import requests
import base64
import json
import os

#databse
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
	db_name = os.environ.get('MONGO_DB_NAME')
	db_collection = os.environ.get('MONGO_COLLECTION_NAME')
	return MongoClient(MONGO_URL)[db_name][db_collection]

def write_to_mongo(object_type, val):
	"""Updates the object_type if it exists with val, otherwise makes
	a new entry into db"""
	
	# get the collection
	collection = get_mongo_collection()
	
	# update/insert relevant documents
	collection.update(
		{ 'key_type': object_type},
		{
			'key_type': object_type,
			'key': val
		},
		upsert=True
	)



def write_to_file(data,filename):
	text_file = open(filename, "w")
	text_file.write(str(data))
	text_file.close()

def reauthenticate():
	refresh_token = get_refresh_token()
	
	# body
	code_payload = {
		"grant_type":"refresh_token",
		"refresh_token":str(refresh_token),
	}
	
	# headers
	base64encoded = base64.b64encode(
		os.environ.get('SPOTIPY_CLIENT_ID') +
		":" +
		os.environ.get('SPOTIPY_CLIENT_SECRET')
	)
	
	headers = {"Authorization":"Basic %s" % base64encoded}
	
	# make the request
	post_request = requests.post(
		"https://accounts.spotify.com/api/token",
		data=code_payload,
		headers=headers
	)
	json_response = json.loads(post_request.text)

	# parse the response
	write_to_file(json_response[u'access_token'], 'auth.txt')
	
	# if a new refresh token is passed save that as well
	if json_response[u'refresh_token']:
		write_to_file(json_response[u'refresh_token'], 'refresh.txt')

def stringify_results(results):
	text_response = "Text back the number of your preffered song or -1 for none of the below: \n"

	for i in range(0,len(results)):
		text_response = text_response + str(i) + ": " + results[i]['name'] + "\n"
	return text_response 