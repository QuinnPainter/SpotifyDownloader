import win32gui
import time
import pyaudio
import wave
import os

folderLocation = "music/"

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def writeToFile(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w+") as o:
        pass
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(data))
    wf.close()
    if os.stat('saveLocation').st_size==0:
        return "fail"
    else:
        return "success"

numFilesSaved = 0
filesFailed = []
input("Ensure no music is playing through Spotify and that the Spotify client is open, then press Enter")
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
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        data = []
        while str(win32gui.GetWindowText(id)) == songName:
            data.append(stream.read(CHUNK))
        saveLocation = folderLocation + songName + ".wav"
        print ("Done recording " + songName + ", saving to " + saveLocation)
        stream.stop_stream()
        stream.close()
        #os.makedirs(os.path.dirname(saveLocation), exist_ok=True)
        #with open(saveLocation, "w+") as o:
        #    pass
        #wf = wave.open(saveLocation, 'wb')
        #wf.setnchannels(CHANNELS)
        #wf.setsampwidth(p.get_sample_size(FORMAT))
        #wf.setframerate(RATE)
        #wf.writeframes(b''.join(data))
        #wf.close()
        if writeToFile(saveLocation, data) == "fail":
            print ("Something went wrong while saving " + songName + "! Trying again...")
            if writeToFile(saveLocation, data) == "fail":
                print ("Failed again. Moving on...")
                filesFailed.append(songName)
                try:
                    os.remove(saveLocation)
                except:
                    print ("Also failed to delete the broken file! Wow. Things must really be screwed up.")
                continue
        numFilesSaved += 1
    print ("Stopping the recording as the playlist ended or was paused")
    print (str(numFilesSaved) + " files were saved")
    if len(filesFailed > 0):
        print ("Failed files: ")
        for f in filesFailed:
            print (f)
    p.terminate()