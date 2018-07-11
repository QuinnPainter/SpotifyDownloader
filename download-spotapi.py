import win32gui
import time
import pyaudio
import wave
import os
import spotipy
import spotipy.util as util
import configreader

savedOptions = configreader.read()
if savedOptions == 0:
    print ("Config file not found! Creating one now.")
    configreader.create()
    print ("See the readme.md for instructions on setting this up.")
    exit()
elif savedOptions == 1:
    print ("Error reading config file!")
    exit()

#Options
username = savedOptions[0]
ClientID = savedOptions[1]
ClientSecret = savedOptions[2]
RedirectURL = savedOptions[3]
folderLocation = savedOptions[4]

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

Scope = "user-read-currently-playing user-modify-playback-state"

token = util.prompt_for_user_token(username, Scope, client_id=ClientID, client_secret=ClientSecret, redirect_uri=RedirectURL)
spot = spotipy.Spotify(auth=token)

def convertToValidPath(path):
    notAllowedCharacters = '\/:*?"<>|'
    filename = path[len(folderLocation):]
    for c in notAllowedCharacters:
        filename = filename.replace(c, "")
    return folderLocation + filename

def checkFileExists(path):
    try:
        if not os.stat(saveLocation).st_size==0:
            return True
    except FileNotFoundError:
        pass
    return False
    
def writeToFile(path, data):
    if checkFileExists(path):
        return "exists"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w+") as o:
        pass
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(data))
    wf.close()
    try:
        if os.stat(saveLocation).st_size==0:
            return "fail"
        else:
            return "success"
    except FileNotFoundError:
        return "fail"

numFilesSaved = 0
filesFailed = []
input("Ensure that some Spotify client is open, then press Enter")
print(spot.currently_playing())
id = win32gui.FindWindow(None, "Spotify")
if (id == 0):
    print ("Spotify not found!")
else:
    print ("Spotify found with an ID of " + str(id))
    print ("Ensure no other sounds play during this process.")
    print ("You can start playing a playlist / song now.")
    print ("Waiting for playback to begin...")
    while win32gui.GetWindowText(id) == "Spotify":
        time.sleep(0.01)
    print ("Playback started with song : " + win32gui.GetWindowText(id))
    while not win32gui.GetWindowText(id) == "Spotify":
        songName = str(win32gui.GetWindowText(id))
        print ("Starting to record " + songName)
        saveLocation = convertToValidPath(folderLocation + songName + ".wav")
        if checkFileExists(saveLocation):
            print ("File " + saveLocation + " already exists! Skipping the song")
            time.sleep(0.5) #If it skips too fast, Spotify freaks out
            #pressButton(Media_Next)
            continue
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        data = []
        while str(win32gui.GetWindowText(id)) == songName:
            data.append(stream.read(CHUNK))
        print ("Done recording " + songName + ", saving to " + saveLocation)
        stream.stop_stream()
        stream.close()
        fileStatus = writeToFile(saveLocation, data)
        if fileStatus == "fail":
            print ("Something went wrong while saving " + songName + "! Trying again...")
            if writeToFile(saveLocation, data) == "fail":
                print ("Failed again. Moving on...")
                filesFailed.append(songName)
                try:
                    os.remove(saveLocation)
                except:
                    print ("Also failed to delete the broken file! Wow. Things must really be screwed up.")
                continue
        elif fileStatus == "exists":
            print ("File " + saveLocation + " already exists! This should never happen??")
            continue
        numFilesSaved += 1
    print ("Stopping the recording as the playlist ended or was paused")
    print (str(numFilesSaved) + " files were saved")
    if len(filesFailed) > 0:
        print ("Failed files: ")
        for f in filesFailed:
            print (f)
    p.terminate()