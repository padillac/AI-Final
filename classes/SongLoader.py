import os.path
import spotipy #library to interact with spotify API
from spotipy.oauth2 import SpotifyClientCredentials #allows authorization to spotify API
import pickle #storing objects in files
from tqdm import tqdm #progress bars
from HiddenPrints import HiddenPrints #stifle built-in print statements



# Object that loads songs either from cached file or from Spotify API.

class SongLoader:

    SPOTIFY_CLIENT_ID='d74eabfa835d4c2a9b2b58b786b6d5ee'
    SPOTIFY_CLIENT_SECRET='759a026c098f40b98583e7c45013ca80'
    SONG_DATA_CACHE_FILE = 'song-data-cache'
    sp = None

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(self.SPOTIFY_CLIENT_ID, self.SPOTIFY_CLIENT_SECRET)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    def loadSongs(self):
        if os.path.isfile(self.SONG_DATA_CACHE_FILE):
            print("song cache file exists. loading song data from:", self.SONG_DATA_CACHE_FILE)
            with open(self.SONG_DATA_CACHE_FILE, 'rb') as songDataFile:
                tracks = pickle.load(songDataFile)
        else:
            print("no cache file found. loading song data from spotify")

            categories = ['US']
            categories += self.sp.categories(country="US", limit=5)['categories']['items']
            categories += ['CA']
            #categories += self.sp.categories(country="CA", limit=50)['categories']['items']
            categories += ['GB']
            #categories += self.sp.categories(country="GB", limit=50)['categories']['items']
            categories += ['FR']
            #categories += self.sp.categories(country="FR", limit=50)['categories']['items']
            categories += ['BR']
            #categories += self.sp.categories(country="BR", limit=50)['categories']['items']
            categories += ['MX']
            #categories += self.sp.categories(country="MX", limit=50)['categories']['items']
            print("found {} categories across 1 countries".format(len(categories)-6))

            print("gathering playlists from categories")
            playlists = []
            for i in tqdm(categories):
                with HiddenPrints():
                    if type(i) == str:
                        countrycode = i
                        continue
                    #stupid regionalmexican never works
                    if i['id'] == 'regionalmexican':
                        continue
                    try:
                        new_playlists = self.sp.category_playlists(i['id'], country=countrycode, limit=20) #change this limit to 50
                    except:
                        continue
                    if new_playlists is not None:
                        playlists += new_playlists['playlists']['items']

            print("gathered {} playlists across all categories".format(len(playlists)))


            tracks = []
            print("gathering tracks from playlists")
            for playlist in tqdm(playlists):
                with HiddenPrints():
                    track_objects = self.sp.user_playlist_tracks('spotify', playlist_id=playlist['id'])['items']
                    if track_objects is not None:
                        for track in track_objects:
                            if track['track'] is None:
                                continue
                            trackData = track['track']
                            trackData.pop('album', None)
                            trackData.pop('available_markets', None)
                            trackData.pop('disc_number', None)
                            trackData.pop('external_ids', None)
                            trackData.pop('preview_url', None)
                            trackData.pop('track_number', None)
                            trackData.pop('episode', None)
                            trackData.pop('is_local', None)
                            trackData.pop('duration_ms', None)

                            audioFeatures = self.sp.audio_features([trackData['id']])[0]
                            trackData['audio_features'] = audioFeatures

                            tracks.append(trackData)


            print("gathered {} tracks across all playlists".format(len(tracks)))

            with open(self.SONG_DATA_CACHE_FILE, 'wb') as songDataFile:
                pickle.dump(tracks, songDataFile)

            print("saved song data to cache file:", self.SONG_DATA_CACHE_FILE)

        print("song data successfully loaded, {} total tracks".format(len(tracks)))

        return tracks
