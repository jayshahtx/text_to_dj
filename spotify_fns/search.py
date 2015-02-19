import spotipy
import pprint
import json
from misc.util import get_auth_token

def search_for_song(song_name):
	# authenticate a spotipy instance
	token = get_auth_token()
	sp = spotipy.Spotify(auth=token)
	results = sp.search(song_name)
	for r in results['tracks']['items']:
		track_title = r['name']
		artist_names = []
		for artist in r['artists']:
			artist_names.append(artist['name'])
		print track_title + " - " + str(artist_names)

	