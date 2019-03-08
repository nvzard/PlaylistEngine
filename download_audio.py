from __future__ import unicode_literals

import youtube_dl

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors' : [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

def downloadAudio(songURL):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(songURL)

downloadAudio(['https://www.youtube.com/watch?v=FxQTY-W6GIo'])
