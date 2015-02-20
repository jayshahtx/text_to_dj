# web protocol
from flask import Flask, request, redirect, g, render_template, session
import requests
import base64
import json
import urllib

# app dependencies
import spotipy
import twilio.twiml

# internal
import os
from spotify_fns import search
from text_fns.handlers import message_handler
from misc.util import write_to_file


# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

# https://whispering-hollows-1165.herokuapp.com
'https://accounts.spotify.com/authorize/redirect_uri=http%3A%2F%2F127.0.0.1%3A8080%2Fcallback%2Fq&response_type=code&client_id=eba5e3a60a524fd996986a4a7b1c91a3'
@app.route('/')
def index():
	root_url = 'https://accounts.spotify.com/authorize/?'
	u = urllib.urlencode({
		'client_id': os.environ.get('SPOTIPY_CLIENT_ID'),
		'response_type': 'code',
		'redirect_uri':os.environ.get('SPOTIPY_REDIRECT_URI'),
		'scope' : 'playlist-modify-public'
	})
	return redirect(root_url + u)

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
    # body = request.values.get('Body', None)

    resp_text = message_handler(request)

    # respond to let sender know message was received
    resp = twilio.twiml.Response()
    resp.message(resp_text)
    return str(resp)

if __name__ == "__main__":
	app.run(debug=True,port=8080)
