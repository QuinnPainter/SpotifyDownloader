import threading
from time import sleep
import spotipy
import spotipy.util as util

Scope = "user-read-currently-playing user-modify-playback-state"

CurrentSongData = ""
spot = ""
ThreadRunning = False

#What the output of CurrentSongData looks like when nothing is playing:
#{'timestamp': -2256, 'context': None, 'progress_ms': 0, 'item': None, 'is_playing': False}

def GetData():
    global CurrentSongData, spot, ThreadRunning
    while ThreadRunning:
        CurrentSongData = spot.currently_playing()
        sleep(1)
        if (CurrentSongData["item"] == None):
            pass
        if (CurrentSongData["is_playing"] == False):
            pass

def Start(user, id, secret, url):
    global spot, ThreadRunning
    token = util.prompt_for_user_token(user, Scope, client_id=id, client_secret=secret, redirect_uri=url)
    spot = spotipy.Spotify(auth=token)
    ThreadRunning = True
    t=threading.Thread(target=GetData)
    t.daemon = True
    t.start()

def Stop():
    ThreadRunning = False

