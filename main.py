import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import os
import spotipy

app = Flask(__name__)

@app.route('/')
def index():
	url1 = 'https://accounts.spotify.com/authorize/?client_id='
	url2 = '&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8080%2Fcallback%2Fq&scope=playlist-modify-public+playlist-modify-private'
	return redirect(url1 + os.environ.get('SPOTIPY_CLIENT_ID') + url2)

@app.route("/callback/q")
def callback():
	access_token = request.args
	code_payload = {
		"grant_type":"authorization_code",
		"code":str(access_token['code']),
		"redirect_uri":os.environ.get('SPOTIPY_REDIRECT_URI')
	}
	base64encoded = base64.b64encode(os.environ.get('SPOTIPY_CLIENT_ID') + ":" + os.environ.get('SPOTIPY_CLIENT_SECRET'))
	headers = {"Authorization":"Basic %s" % base64encoded}
	post_request = requests.post("https://accounts.spotify.com/api/token",data=code_payload,headers=headers)
	json_response = json.loads(post_request.text)
	
	token = json_response[u'access_token']
	# at some point, we will want to render_template ("auth_successful_page.html") after we design it
	
	# dummy code do demonstrate how spotipy works
	sp = spotipy.Spotify(auth=token)
	playlists = sp.user_playlists('jayshahtx')
	for playlist in playlists['items']:
		if playlist['owner']['id'] == 'jayshahtx':
			print
			print playlist['name']

	return ("Authentication was successful!")

if __name__ == "__main__":
	app.run(debug=True,port=8080)
