from bilibili_api.live import LiveDanmaku
from decouple import config
import Spotify
import os

# parse the incoming msg
def parseMsg(msg):
    this = msg['data']['info'][1]
    if this[0] == "!" or this[0] == '！':
        # in the case the new msg is a command msg, call command function
        command(this[1:])
    else:
        pass

def command(msg):
    try:
        # if the incoming message is a song request
        if msg[:2] == '点歌':
            Bot.requestSong(msg[3:])
    except:
        pass

# Initialize Spotipy
Bot = Spotify.Bot()

# Initialize LiveDanmuku
roomID = config('bilibili_room_id')
thisRoom = LiveDanmaku(room_display_id=roomID)

# Add new handler
thisRoom.add_event_handler(event_name='DANMU_MSG', func=parseMsg)


if __name__ == '__main__':
    try:
        os.mkdirs(config('cache_dir'))
        queue = open(cacheDir+'\cache.txt', 'w')
        queue.close()
    except:
        pass

    thisRoom.connect()
