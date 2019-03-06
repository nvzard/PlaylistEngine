import spotipy
import spotipy.oauth2 as oauth2
import lyricwikia
from titlecase import titlecase

def generate_token():
    credentials = oauth2.SpotifyClientCredentials(
        client_id="4fe3fecfe5334023a1472516cc99d805",
        client_secret="0f02b7c483c04257984695007a4a8d5c",
    )
    token = credentials.get_access_token()
    return token

def refresh_token():
    global spotify
    new_token = generate_token()
    spotify = spotipy.Spotify(auth=new_token)

_token = generate_token()
spotify = spotipy.Spotify(auth=_token)

def generate_metadata(raw_song):

    # meta_tags = spotify.track(raw_song)
    meta_tags = spotify.search(raw_song, limit=1)["tracks"]["items"][0]
    artist = spotify.artist(meta_tags["artists"][0]["id"])
    album = spotify.album(meta_tags["album"]["id"])

    try:
        meta_tags[u"genre"] = titlecase(artist["genres"][0])
    except IndexError:
        meta_tags[u"genre"] = None
    try:
        meta_tags[u"copyright"] = album["copyrights"][0]["text"]
    except IndexError:
        meta_tags[u"copyright"] = None
    try:
        meta_tags[u"external_ids"][u"isrc"]
    except KeyError:
        meta_tags[u"external_ids"][u"isrc"] = None

    meta_tags[u"release_date"] = album["release_date"]
    meta_tags[u"publisher"] = album["label"]
    meta_tags[u"total_tracks"] = album["tracks"]["total"]

    try:
        meta_tags["lyrics"] = lyricwikia.get_lyrics(
            meta_tags["artists"][0]["name"], meta_tags["name"]
        )
    except lyricwikia.LyricsNotFound:
        meta_tags["lyrics"] = None

    return meta_tags

def main():
    string = "God's Plan"
    print(generate_metadata(string))

main()
