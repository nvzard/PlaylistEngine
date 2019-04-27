from __future__ import unicode_literals

import youtube_dl

ydl_opts = {
        'format': 'bestaudio/best',
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

def downloadAudio(songURL):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(songURL)

downloadAudio(['https://www.youtube.com/watch?v=FxQTY-W6GIo'])
