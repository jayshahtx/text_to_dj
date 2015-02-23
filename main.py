# web protocol
from flask import Flask, request, redirect, g, render_template, session
import urllib

# app dependencies
import twilio.twiml

# internal
import os
from text_fns.handlers import message_handler
from misc.auth import authenticate


# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
	"""Start authentication process by having user log in to Spotify"""
	# login to spotify
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
	"""Finish the authentication process via a callback"""
	# parse the token and authenticate with it
	access_token = str(request.args['code'])
	try:
		authenticate(access_token)
		return "Authentication was successful!"
	except:
		return "Authentication unsuccessful"


@app.route("/twilio", methods=['GET', 'POST'])
def respont_to_text():
    """Respond to incoming song requests"""

    # generate response to incoming message and reply to user
    resp_text = message_handler(request)
    resp = twilio.twiml.Response()
    resp.message(resp_text)
    return str(resp)

if __name__ == "__main__":
	app.run(debug=True,port=8080)
