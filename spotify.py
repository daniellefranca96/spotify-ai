import os
import logging

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()


class Spotify:
    REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", 'https://rcot-ui.fly.dev')
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SCOPES = [
        'ugc-image-upload',
        'user-read-playback-state',
        'user-modify-playback-state',
        'user-read-currently-playing',
        'app-remote-control',
        'streaming',
        'playlist-read-private',
        'playlist-read-collaborative',
        'playlist-modify-private',
        'playlist-modify-public',
        'user-follow-modify',
        'user-follow-read',
        'user-read-playback-position',
        'user-top-read',
        'user-read-recently-played',
        'user-library-modify',
        'user-library-read',
        'user-read-email',
        'user-read-private'
    ]

    def __init__(self):
        self.sp_oauth = SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                     client_secret=self.SPOTIPY_CLIENT_SECRET,
                                     redirect_uri=self.REDIRECT_URI,
                                     scope=" ".join(self.SCOPES))
        self.check_auth()
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)
        logging.basicConfig(level=logging.INFO)

    def call_method(self):
        return {
            "start_playback": {"method": self.start_playback,
                               "description": "Provide a uri to start playback of an album, artist, or playlist.",
                               "parameters": {"uri": {"type": "string", "description": "Spotify uri of the content"},
                                              "type_context": {"type": "string",
                                                               "description": "Spotify type_context can be one of this options only track/episode/album/playlist/podcast and must always be reference to the context of the uri being played"},
                                              "offset": {"offset": "number",
                                                         "description": "Spotify offset can be time/position, must always start at 0"},
                                              "device_id": {"device_id": "number",
                                                            "description": "Spotify device id, send -1 to ask for current device"}
                                              }},
            "search": {"method": self.search, "description": "Search for a song/artist/album/podcast/episode",
                       "parameters": {"query": {"type": "string", "description": "Search query"},
                                      "type": {"type": "string",
                                               "description": "Search type ['track', 'artist', 'album', 'show', 'episode']"}},
                       "add_fields": {"type": "list", "description": "additional avaliable fields to put in result"},
                       "keys": {"type": "boolean",
                                "description": "if true will return only the avaliables keys for result"}
                       },
            "devices": {"method": self.devices, "description": "Get all devices of the current user",
                        "parameters": None},
            "pause": {"method": self.pause, "description": "Pause playback", "parameters": None},
            "shuffle": {"method": self.shuffle, "description": "Shuffle the queue",
                        "parameters": {"state": {"state": "boolean", "description": "True or False"}}},
            "repeat": {"method": self.shuffle, "description": "Repeat the queue",
                       "parameters": {"state": {"state": "boolean", "description": "True or False"}}},
            "current_user_recently_played": {"method": self.current_user_recently_played,
                                             "description": "Get recently played songs from the user",
                                             "parameters": None},
            "next": {"method": self.next_track, "description": "Skip to the next item",
                     "parameters": {"device_id": {"device_id": "number",
                                                  "description": "Spotify device id, send -1 to ask for current device"}}},
            "previous": {"method": self.previous_track, "description": "Skip to the previous item",
                         "parameters": {"device_id": {"device_id": "number",
                                                      "description": "Spotify device id, send -1 to ask for current device"}}},
            "get_playlists": {"method": self.get_playlists, "description": "Get all playlists of the current user",
                              "parameters": None},
            "get_playlist": {"method": self.get_playlist,
                             "description": "Get a specific playlist, the pool of tracks is 5 per request",
                             "parameters": {"playlist_id": {"type": "string", "description": "Spotify playlist id"},
                                            "offset": {"type": "number",
                                                       "description": "from where to start the list of tracks"}},
                             },
            "get_artist": {"method": self.get_artist, "description": "Get information about an artist",
                           "parameters": {"artist_id": {"type": "string", "description": "Spotify artist id"}}},
            "get_podcasts": {"method": self.get_podcasts, "description": "Get all podcasts of the current user",
                             "parameters": None},
            "get_album": {"method": self.get_album, "description": "Get a album by its id",
                          "parameters": {"album_id": {"type": "string", "description": "album spotify id"}}}
        }

    def devices(self):
        return self.sp.devices()

    def get_album(self, album_id):
        album = {'artists': [], 'tracks': []}
        result = self.sp.album(album_id)

        album['name'] = result['name']

        for a in result['artists']:
            album['artists'].append(a['name'])

        album['tracks'] = self.extract_info(result['tracks']['items'], [])

        return album

    def current_playback(self):
        return self.sp.current_playback()

    def get_device(self, device):
        if device == -1:
            current = self.sp.current_playback()
            if current is None:
                return 0
            else:
                return current['device']['id']
        return device if device is not None else 0

    def start_playback(self, uri, type_context, offset=0, device_id=0):
        current = self.sp.current_playback()

        device_id = self.get_device(device_id)
        offset = offset if offset is not None else 0

        if current is not None and current['is_playing']:
            self.sp.pause_playback()
            device_id = 0

        if type_context in ["track", "episode"]:
            self.sp.start_playback(device_id, uris=[uri], offset={"position": offset})
        else:
            self.sp.start_playback(device_id, context_uri=uri, offset={"position": offset})
        return "Playing the song/episode"

    def pause(self):
        self.sp.pause_playback()
        return "Paused"

    def repeat(self, state):
        self.sp.repeat(state)
        return "Repeated"

    def shuffle(self, state):
        self.sp.shuffle(state)
        return "Shuffled"

    def add_to_queue(self, track_id):
        self.sp.add_to_queue(track_id)

    def get_playlists(self):
        return self.extract_info(self.extract_info(self.sp.current_user_playlists()['items'], []), [])

    def get_playlist(self, playlist_id, offset=0):
        return self.extract_info(self.sp.playlist_items(playlist_id=playlist_id, offset=offset, limit=5)['items'], [],
                                 'track')

    def get_artist(self, artist_id):
        return self.sp.artist(artist_id)

    def get_podcasts(self):
        return self.extract_info(self.sp.current_user_saved_shows()['items'], ['description'], 'show')

    def extract_info_one(self, origin, add_fields):

        data = {
            'name': origin['name'],
            'id': origin['id'],
            'uri': origin['uri']
        }

        for f in add_fields:
            data[f] = origin[f]
        print(data)

        return data

    def extract_info(self, data_list, add_fields, subfield=None):

        info_list = []

        for data in data_list:
            if subfield is None:
                track_info = self.extract_info_one(data, add_fields)
            else:
                track_info = self.extract_info_one(data[subfield], add_fields)
            info_list.append(track_info)

        return info_list

    def search(self, query, type="track", add_fields=None, keys=False):
        """Searches for songs, artists, albums, podcasts, episodes, etc. on Spotify."""
        if add_fields is None:
            add_fields = []

        result = self.sp.search(query, type=type, limit=5)
        type_dict = {"track": "tracks", "artist": "artists", "show": "shows", "episode": "episodes", "album": "albums",
                     "playlist": "playlists", "audiobook": "audiobooks"}
        if type not in type_dict.keys():
            logging.error("Invalid type for search")
            return None
        result_f = self.extract_info(result[type_dict[type]]['items'], add_fields)

        if keys:
            return result[type + "s"]['items'][0].keys()
        return result_f

    def queue(self):
        return self.sp.queue()

    def current_user_recently_played(self):
        return self.extract_info(self.sp.current_user_recently_played()['items'], [], 'track')

    def next_track(self, device_id):
        device_id = self.get_device(device_id)
        self.sp.next_track(device_id)
        return "Next item playing"

    def previous_track(self, device_id):
        device_id = self.get_device(device_id)
        self.sp.previous_track(device_id)
        return "Previous item playing"

    def set_code_auth_url(self, code):
        self.sp_oauth.get_access_token(code)
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

    def get_url_authenticate(self):
        return self.sp_oauth.get_authorize_url()

    def check_auth(self):
        token_info = self.sp_oauth.get_cached_token()

        if not token_info:
            return False
        else:
            if self.sp_oauth.is_token_expired(token_info):
                self.sp_oauth.refresh_access_token(token_info['refresh_token'])
        return True
