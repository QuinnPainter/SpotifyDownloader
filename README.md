# SpotifyDownloader
A simple, Python-based mechanism for getting local copies of your Spotify songs and playlists. Functions by looking at your currently playing song, and recording your audio loopback (commonly called "Stereo Mix" or "What U Hear"). Currently only has a terminal interface and saves all songs as .wav only. Currently only tested on Windows 10 x64.

There are two version that can be used:
- The win32api version uses the title of the Spotify window to determine currently playing song. As a result, there is no metadata saved with each song, and this method tends to be less reliable. However, you do not have to grant access to your Spotify account. Only compatible with Windows.
- The Spotify API version uses the Spotify Web API to determine the currently playing song, and has more advanced features like metadata collection. Slightly more difficult to set up, but is more advanced and more reliable. Also has the benefit that it should run on anything that can run Spotify and Python. (Must use this one if using Mac/Linux)

### Requirements:
- [Python 3] (https://www.python.org/downloads/)
- [pywin32] (https://github.com/mhammond/pywin32) - Only required for the win32api version
- [pyaudio] (https://github.com/jleb/pyaudio)
- [spotipy] (https://github.com/plamere/spotipy) - Only required for Spotify API version

### Setup

Install `python3` and `pip`

Use `pip install pyaudio` to install pyaudio.
If using the win32api version, run 'pip install pywin32'
This command requires [Visual Studio 2017 C++ Build Tools] (https://visualstudio.microsoft.com/downloads/) to be installed.

If using the spotify API version, run 'pip install git+https://github.com/plamere/spotipy.git --upgrade'
This is important, as running 'pip install spotipy' will not work. The version in pip is outdated, and will not work.

### Usage

`coming soon`

### Why does this exist?

There are many other Spotify downloaders, but all of them (that I've seen) rely on using Youtube to download the songs. This can lead to inaccurate downloads, and sometimes the song isn't on YouTube at all.
This aims to fix that problem by directly recording the songs straight from Spotify, eliminating any inaccuracies and guaranteeing what you download is exactly the same as what you hear.
This comes at the downside that downloading the songs takes as long as it takes to play through them, so for longer playlists this process can take hours.