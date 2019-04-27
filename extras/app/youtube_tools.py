from __future__ import unicode_literals

import re
import requests
import youtube_dl
import pafy

from bs4 import BeautifulSoup

# YOUTUBE_API_KEY = 'AIzaSyBnZ_Fys6No6B4TvZPE3vGP3P6RJeeXLHY'
# Playlist URL
# https://www.youtube.com/playlist?list=PLlcPcYKglprWUIqTBoEU9fInqJym3yfmt

playlist_url = 'https://www.youtube.com/playlist?list=PLlcPcYKglprUEISB4RoEC9j4de30_CBJZ'

ydl_opts = {
        'format': 'bestaudio/best',
        # 'quite': True,
        'outtmpl': '%(title)s.%(ext)s',
        'writethumbnail': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {
            'key': 'FFmpegMetadata',
        },
        {
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': True,  # overwrite any thumbnails already present
        },
        ],
}

def formatting(songName):
    # remove brackets
    songName = re.sub("[\(\[].*?[\)\]]", "", songName)
    # remove emoticons
    songName = re.sub(r'[^\x00-\x7f]', '', songName)
    return songName

def get_list_of_songs(playlist):
    '''
    playlist: url of the playlist

    return a dictionary(songName:songURL)
    '''
    page = requests.get(playlist).text
    soup = BeautifulSoup(page, 'html.parser')
    songsAndUrls = {}
    domain = 'https://www.youtube.com'
    for link in soup.find_all('a', {'dir': 'ltr'}):
        href = link.get('href')
        if href.startswith('/watch?'):
            song_name = formatting(link.string.strip())
            song_link = domain + href
            # To remove playlist link from the url
            song_link = song_link.split('&', 1)[0]
            songsAndUrls[song_name] = song_link

    return list(songsAndUrls.values())

def getTrackInfo(url):
    return pafy.new(url)

def downloadAudio(songsList, opts):
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download(songsList)

# print()
# downloadAudio(get_list_of_songs(playlist_url), ydl_opts)

#for name, url in get_list_of_songs(playlist_url).items():
#    print(name)
#    print(url)
#    print()

# downloadAudio(['https://www.youtube.com/watch?v=FxQTY-W6GIo'])
