from flask import request, session, Flask
from spotify_fns.search import search_for_song, update_playlist
from misc.util import stringify_results


# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

def message_handler(req):
	body = req.values.get('Body', None)
	
	# this is a response
	try:
		float(body)
		return handle_song_response(body)
	
	# this is a song name
	except ValueError:
		return handle_song_name(body)


def handle_song_response(body):
	index = int(str(body))
	song_history = session.get('song_history', None)
	if song_history:
		return update_playlist(song_history[-1][index])
	else:
		return "You must first search for a song, please respond with a song name"

def handle_song_name(body):
	# get the results of this query in JSON
	search_result = search_for_song(body)		
	text_response = stringify_results(search_result)

	# update this user's cookies to store these results
	song_history = session.get('song_history', [])
	song_history.append(search_result)
	session['song_history'] = song_history	

	return text_response