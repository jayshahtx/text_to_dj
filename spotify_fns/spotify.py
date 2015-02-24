import spotipy
import pprint
import json
import os
from misc.auth import authenticate
from db_fns.db import get_auth_token


def get_spotipy():
	"""Function which returns an authenticated spotipy instance"""
	# check if we need to reauth
	try:
		token = get_auth_token()
		sp = spotipy.Spotify(auth=token)
		# try searching, we don't care for results
		sp.search("test")
		return sp

	# perform re-auth and try again
	except:
		# refresh tokens
		authenticate()
		token = get_auth_token()
		sp = spotipy.Spotify(auth=token)
		
		# try searching, we don't care for results
		sp.search("test")
		return sp

def search_for_song(song_name):
	
	def get_artists(artists):
		"""Method to stringify artists from JSON"""
		output = ""
		for artist in artists:
			output += artist['name'].encode('utf-8') + ", "

		#delete the trailing comma/extra space
		output = output[:-2]
		return output

	def parse_results(results):
		top_results = results['tracks']['items']
		response = []
		
		# store the top 5 results
		for i in range (0,5):
			list_item = {}
			list_item['name'] = top_results[i]['name']
			list_item['artists'] = get_artists(top_results[i]['artists'])
			list_item['track_id'] = top_results[i]['id']
			response.append(list_item)

		return response
	
	sp = get_spotipy()
	results = sp.search(song_name)
	return parse_results(results)
		

def update_playlist(json_song):
	"""Updates spotify playlist from JSON data that is passed in"""

	sp = get_spotipy()

	#user params
	track_id = json_song['track_id']
	playlist_id = os.environ.get('SPOTIFY_PLAYLIST_ID')
	user_id = os.environ.get('SPOTIFY_USER_ID')

	#update playlist
	results = sp.user_playlist_add_tracks(user_id, playlist_id, [track_id])

	#generate response
	if results['snapshot_id']:
		return "'%s' by %s was successfully added to your playlist"%(
			json_song['name'].encode('utf-8'),
			json_song['artists']
		)
	else:
		return "Sorry, there was an error in search.update_playlist"