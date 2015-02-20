import requests
import base64
import json
import os

def get_auth_token():
	"""Reads in auth token from text file"""
	auth = open('auth.txt', 'r')
	a = auth.read()
	return a

def get_refresh_token():
	"""Reads in refresh token from text file"""
	auth = open('refresh.txt','r')
	a = auth.read()
	return a

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

def stringify_results(results):
	text_response = "Text back the number of your preffered song or -1 for none of the below: \n"

	for i in range(0,len(results)):
		text_response = text_response + str(i) + ": " + results[i]['name'] + "\n"
	return text_response 