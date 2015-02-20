# web protocol
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import json

# app dependencies
import spotipy
import twilio.twiml

# internal
import os
from spotify_fns import search
from misc.util import write_to_file

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
	
	# for now write the token to a text file, move to SQL later
	write_to_file(json_response[u'access_token'], 'auth.txt')
	write_to_file(json_response[u'refresh_token'], 'refresh.txt')

	# at some point, we will want to render_template ("auth_successful_page.html") after we design it
	return ("Authentication was successful!")

# build out this function later, see this url
def refresh_token():
	pass

@app.route("/twilio", methods=['GET', 'POST'])
def respont_to_text():
    """Respond to incoming calls with a simple text message."""
    
    # search for a song name and print results
    body = request.values.get('Body', None)
    search_result = search.search_for_song(body)

    # respond to let sender know message was received
    resp = twilio.twiml.Response()
    resp.message(search_result)
    return str(resp)

if __name__ == "__main__":
	app.run(debug=True,port=8080)
