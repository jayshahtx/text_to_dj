import spotipy
import pprint
import json
import os
from misc.auth import authenticate

from db_fns.db import get_auth_token, check_token_exp


def get_spotipy():
	"""Function which returns an authenticated spotipy instance"""
	
	token = get_auth_token()
	sp = spotipy.Spotify(auth=token)
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

		max_range = min(5,len(top_results))
		
		# store the top 5 results
		for i in range (0,max_range):
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

	#playlist URL
	playlist_url = (
		'http://open.spotify.com/user/' + 
		os.environ.get('SPOTIFY_USER_ID') + 
		'/playlist/' + 
		os.environ.get('SPOTIFY_PLAYLIST_ID')
	)


	#generate response
	if results['snapshot_id']:
		return "'%s' by %s was successfully added to the playlist, you can view it here %s"%(
			json_song['name'].encode('utf-8'),
			json_song['artists'],
			playlist_url
		)
	else:
		return "Sorry, there was an error in search.update_playlist"