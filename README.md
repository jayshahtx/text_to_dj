#Text to DJ#

Text to DJ is an application that lets users text a song name to a phone number and update a playlist with that song. Check out the screenshots below or try it yourself by texting a song name to 781-916-8742 and update [this playlist][4].

1) Text a song name | 2) Select a song | 3) Playlist will be updated
:-------------------------:|:-------------------------:|:-------------------------:
![][1]  |  ![][2] | ![][3]

##How does it work?##
Text messages are recieved and sent via [Twilio's][5] API and song/playlist functionality is handled via [Spotify's][6] API. 

##Key technologies##
1. Gunicorn to manage a web server
2. Flask to handle routing on the server
3. MongoDB to store/update Spotify auth credentials
4. Twilio API (Twilio)
5. Spotify API (Spotipy)

## Required accounts/setup ##
1. Register for a [Twilio][7] account (Free trial) 
2. Register a [Spotify application][8]
3. Create a [Heroku account][11] and [install toolbelt][9]
4. Add [MongoDB][10] as an addon to your heroku account

## Set up ##

Each of the four steps above will produce some sort of credentials that you'll need to store for your program to work correctly. Create a new [config variable][12] in your Heroku app fo reach of these variables. **Note: this is not secure** but will suffice for the time being. Create the following config variables:

<pre><code>
export SPOTIPY_CLIENT_ID='Client ID from Spotify'
export SPOTIPY_CLIENT_SECRET='Client secret from Spotify'
export SPOTIPY_REDIRECT_URI='your_heroku_app.herokuapp.com/callback/q'
export MONGOHQ_URL='mongodb://user:user@99999.mongolab.com:99999/your_app' #update this URL with your app's info
export MONGO_DB_NAME='this is the suffix to your MongoHQURL, usually starts with 'heroku_app'>
export MONGO_COLLECTION_NAME='auth_properties' #can leave the same
export SPOTIFY_PLAYLIST_ID='spotify_playlist_id'
export SPOTIFY_USER_ID='your_spotify_account_name'
</code></pre>

Update your Twilio app's messaging URL to ensure that Twilio actually hits your server:
![][13]

## Notes ##
If you have trouble getting this app set up, please feel free to send me a message. This app was my first foray into server side development and working with authentication/callbacks. As a result, I'm fairly positive I went against some best practicies - your feedback is welcome!

As an aside, a feature I'd like to build (time permitting) is an admin option which texts the owner of the playlist for permission each time someone makes a request to update the playlist - feel free to beat me to it!

[1]:http://i.imgur.com/y6daUDV.png?1
[2]:http://i.imgur.com/yaxqYBc.png?1
[3]:http://i.imgur.com/FNaYzeI.png?1
[4]:http://open.spotify.com/user/jayshahtx/playlist/2OPixCtmCxev1tnBTEAzGd
[5]:https://www.twilio.com/api
[6]:https://developer.spotify.com/web-api/
[7]:https://developer.spotify.com/web-api/
[8]:https://developer.spotify.com/my-applications/#!/applications/create
[9]:https://devcenter.heroku.com/articles/getting-started-with-python#set-up
[10]:https://addons.heroku.com/mongolab
[11]:https://heroku.com
[12]:https://devcenter.heroku.com/articles/config-vars
[13]:http://i.imgur.com/e8lA14T.png?1
