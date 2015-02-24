# url navigation
import requests
import base64
import json
import urllib
import os

# mongo fns
from db_fns.db import write_to_mongo, get_refresh_token

def get_code_paylod(access_token):
	if not access_token:
		refresh_token = get_refresh_token()
		code_payload = {
			"grant_type":"refresh_token",
			"refresh_token":refresh_token,
		}
	else:
		code_payload = {
			"grant_type":"authorization_code",
			"code":access_token,
			"redirect_uri":os.environ.get('SPOTIPY_REDIRECT_URI')
		}
	return code_payload

def authenticate(access_token=None):
	"""Method which gets new API credentials to Spotify and updates Mongo DB
		with the newest keys"""

	code_payload = get_code_paylod(access_token)
	base64encoded = base64.b64encode(
		os.environ.get('SPOTIPY_CLIENT_ID') + 
		":" + 
		os.environ.get('SPOTIPY_CLIENT_SECRET')
	)

	headers = {"Authorization":"Basic %s" % base64encoded}
	post_request = requests.post(
		"https://accounts.spotify.com/api/token",
		data=code_payload,
		headers=headers
	)
	
	json_response = json.loads(post_request.text)
	print json.dumps(json_response, indent=1)
	# write the new access token to mongo db
	write_to_mongo('access_token', json_response[u'access_token'])

	# if a refresh token is passed, write that as well
	if json_response[u'refresh_token']:
		write_to_mongo('refresh_token', json_response[u'refresh_token'])

	return True