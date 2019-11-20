import spotipy #library to interact with spotify API
from spotipy.oauth2 import SpotifyClientCredentials

import pickle #storing objects in files
import os.path
import tqdm #progress bars

#global variables
CLIENT_ID='d74eabfa835d4c2a9b2b58b786b6d5ee'
CLIENT_SECRET='759a026c098f40b98583e7c45013ca80'

SONG_DATA_CACHE_FILE = 'song-data-cache'




client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




if os.path.isfile(SONG_DATA_CACHE_FILE):
    print("cache file exists. loading song data from:", SONG_DATA_CACHE_FILE)
    with open(SONG_DATA_CACHE_FILE, 'rb') as songDataFile:
        tracks = pickle.load(songDataFile)
else:
    print("no cache file found. loading song data from spotify")

    categories = []
    categories += sp.categories(country="US", limit=50)['categories']['items']
    #categories += sp.categories(country="CA", limit=50)['categories']['items']
    #categories += sp.categories(country="GB", limit=50)['categories']['items']
    #categories += sp.categories(country="FR", limit=50)['categories']['items']
    #categories += sp.categories(country="BR", limit=50)['categories']['items']
    #categories += sp.categories(country="MX", limit=50)['categories']['items']

    print("found {} categories".format(len(categories)))


    playlists = []
    for i in categories:
        print(i['id'])
        new_playlists = sp.category_playlists(i['id'], country='US', limit=50)
        print(type(new_playlists))
        if new_playlists is None:
            print("query failed")
        else:
            playlists += new_playlists['playlists']['items']


    print("gathered {} playlists across all categories".format(len(playlists)))


    tracks = []
    for playlist in playlists:
        #print(playlist['uri'],  playlist['name'])
        tracks += sp.user_playlist_tracks('spotify', playlist_id=playlist['id'])['items']


    print("gathered {} tracks across all playlists".format(len(tracks)))

    with open(SONG_DATA_CACHE_FILE, 'wb') as songDataFile:
        pickle.dump(tracks, songDataFile)

    print("saved song data to cache file:", SONG_DATA_CACHE_FILE)




print("song data loaded, {} total tracks".format(len(tracks)))

for track in tracks:
    print(track['uri'], track['name'])
