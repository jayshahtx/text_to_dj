import spotipy
import pprint
import json
from misc.util import get_auth_token

def search_for_song(song_name):
	
	def get_artists(artists):
		"""Method to stringify artists from JSON"""
		output = ""
		for artist in artists:
			output += artist['name'].encode('utf-8') + ", "

		#delete the trailing comma/extra space
		output = output[:-2]
		return output

	# authenticate a spotipy instance
	token = get_auth_token()
	
	try:
		sp = spotipy.Spotify(auth=token)
		results = sp.search(song_name)
	except:	
		return "Sorry, your account is not authenticated"

	
	top_results = results['tracks']['items']
	top_result = top_results[0]

	# print the top 5 results
	for i in range (0,5):
		title = top_results[i]['name']
		artists = get_artists(top_results[i]['artists'])
		print title + " - " + artists

	# extract the parameters
	title = top_result['name']
	artists = get_artists(top_result['artists'])
	track_id = top_result['id']

	#user params
	playlist_id = '2OPixCtmCxev1tnBTEAzGd'
	user_id = 'jayshahtx'

	#update playlist
	results = sp.user_playlist_add_tracks(user_id, playlist_id, [track_id])
	
	#generate response
	if results['snapshot_id']:
		return "'%s' by %s was successfully added to your playlist"%(
			top_result['name'].encode('utf-8'),
			get_artists(top_result['artists'])
		)
	else:
		return "Sorry, there was an error with your search"