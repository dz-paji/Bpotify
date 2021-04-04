import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

# speficy the permission needed
scope = 'user-modify-playback-state'

cacheDir = config('cache_dir')

class Bot():
    def __init__(self):
        id = config('client_id')
        secret = config('client_secret')
        uri = config('redirect_uri')
        scope = 'user-modify-playback-state'
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=id, client_secret=secret, redirect_uri=uri))

    def requestSong(self, criteria):
        isFound = False
        # According to Spotify seaching guidelines, space should be replaced by `+` or `%20`
        searchQ = criteria.replace(' ', '+')

        # obtain the first searching result
        results = self.spotify.search(q=searchQ, type='track', limit=1, offset=0)

        # do a small linear search if the first track isnt what we intended to find
        # you can incrase the range if youd like to
        # finding a less popular song may require more searching cycles
        for i in range(0, 5):
            if results['tracks']['items'][0]['name'].lower() == criteria.lower():
                id = results['tracks']['items'][0]['id']
                isFound = True
                break
            else:
                results = self.spotify.search(q=searchQ, type='track', limit=1, offset=i)
        
        if isFound == True:
            self.spotify.add_to_queue(id)
            print('200')
            queue = open(cacheDir+'\cache.txt', 'a+', encoding='utf8')
            print('歌曲', results['tracks']['items'][0]['name'], '已加入播放列表')
            record = '歌曲 ' + results['tracks']['items'][0]['name'] + ' 已加入播放列表 \n' 
            queue.write(record)
            queue.close()
            sleep(10)
            queue = open(cacheDir+'\cache.txt', 'w')
            queue.close()
        else:
            print('404')

if __name__ == '__main__':
    This = Bot()
    This.requestSong('fly away')
