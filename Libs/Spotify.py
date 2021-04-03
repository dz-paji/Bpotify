import spotipy
import json
from decouple import config
from spotipy.oauth2 import SpotifyOAuth

# speficy the permission needed
scope = 'user-modify-playback-state'


class Bot():
    def __init__(self):
        id = config('client_id')
        secret = config('client_secret')
        uri = config('redirect_uri')
        scope = 'user-modify-playback-state'
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=id, client_secret=secret, redirect_uri=uri))

    def requestSong(self, criteria):
        # According to Spotify seaching guidelines, space should be replaced by `+` or `%20`
        searchQ = criteria.replace(' ', '+')

        # obtain the first searching result
        results = self.spotify.search(q=searchQ, type='track', limit=1, offset=0)

        # do a small linear search if the first track isnt what we intended to find
        # you can incrase the range if youd like to
        # finding a less popular song may require more searching cycles
        for i in range(1, 5):
            if results['tracks']['items'][0]['name'].lower() == criteria.lower():
                id = results['tracks']['items'][0]['id']
                isFound = True
                break
            else:
                results = self.spotify.search(q=searchQ, type='track', limit=1, offset=i)
        
        if isFound == True:
            self.spotify.add_to_queue(id)
            return 200
        else:
            return 404

if __name__ == '__main__':
        This = Bot()
        This.requestSong('what you know')