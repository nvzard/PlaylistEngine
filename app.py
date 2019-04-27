from __future__ import unicode_literals

import random
import shutil
import os
import glob
import zipfile

from multiprocessing import Process
from flask import Flask, jsonify, request, send_from_directory
from youtube_tools import *

app = Flask(__name__)
app.debug = True

# /home/vzard/Desktop/DopeStuff/MinorProject
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = BASE_DIR + '/data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def remove_dir(dirpath):
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print('Removing Existing dir {}'.format(dirpath))
        shutil.rmtree(dirpath)

def process_request(request_id, playlist_url):
    songs = get_list_of_songs(playlist_url)
    print(songs)
    download_path = DATA_DIR + '/' + request_id
    print(download_path)
    remove_dir(download_path)
    os.makedirs(download_path)
    options  = ydl_opts
    options['outtmpl'] = download_path + '/%(title)s.%(ext)s'
    print('Downloading Audio for {}'.format(request_id))
    downloadAudio(songs, options)
    print("Download Audio for {}".format(request_id))
    print("Deleting Thumbnails for {}".format(request_id))
    for image in glob.glob(download_path + '/*.jpg'):
        os.remove(image)
    print("Deleted Thumbnails for {}".format(request_id))
    print("Making Archive..")
    shutil.make_archive(download_path, 'zip', download_path)
    print("Zip Done")
    remove_dir(download_path)

@app.route("/request", methods=['GET', 'POST'])
def first_contact():
    if request.method == 'GET':
        return 'No support for GET requests my friend :)'
    else:
        data = request.get_json(force=True)
        playlist_url = data.get('url')
        request_id = str(random.randint(1, 56999))
        response = {
            str('url'): str(playlist_url),
            str('id'): str(request_id),
        }
        print(response)
        process = Process(target=process_request, args=(request_id, playlist_url))
        process.start()
        print("Process Started..")
    return jsonify(response)

@app.route("/download/<path:path>", methods=['GET', 'POST'])
def download(path):
    filename = path + '.zip'
    file_path = DATA_DIR + '/' + filename
    if os.path.exists(file_path):
        return send_from_directory(DATA_DIR, filename, as_attachment=True)
        return
    else:
        return 'File Does Not Exists', 404

@app.route("/")
def welcome():
    return "<h1>Welcome to the Server</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT'), threaded=True)

