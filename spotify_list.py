
import spotipy
from spotipy import util
from spotipy.client import SpotifyException
from collections import Counter
from gensim.utils import tokenize
import time
import tqdm
import json

CLIENT_ID = 'your user id'
CLIENT_SECRET = 'your secret key'  #check sporify developer account
USER_ID = 'enkaranfiles'

token = util.prompt_for_user_token(USER_ID, '',
                                   client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                   redirect_uri='http://127.0.0.1:8000/callback') # also you need to add this url whitelist in your account
session = spotipy.Spotify(auth=token)


def find_playlists(session, w, max_count=5000):
    try:
        res = session.search(w, limit=50, type='playlist')
        while res:
            for playlist in res['playlists']['items']:
                yield playlist
                max_count -= 1
                if max_count == 0:
                    raise StopIteration
            tries = 3
            while tries > 0:
                try:
                    res = session.next(res['playlists'])
                    tries = 0
                except SpotifyException as e:
                    tries -= 1
                    time.sleep(0.2)
                    if tries == 0:
                        raise
    except SpotifyException as e:
        status = e.http_status
        if status == 404:
            raise StopIteration
        raise

for pl in find_playlists(session, 'summer'):
    break


word_counts = Counter({'a': 1})
playlists = {}
words_seen = set()
playlists = {}
count = 0
dupes = 0


while len(playlists) < 100000:
    for word, _ in word_counts.most_common():
        if not word in words_seen:
            words_seen.add(word)
            print('word>', word)
            for playlist in find_playlists(session, word):
                if playlist['id'] in playlists:
                    dupes += 1
                elif playlist['name'] and playlist['owner']:
                    playlists[playlist['id']] = {
                      'owner': playlist['owner']['id'],
                      'name': playlist['name'],
                      'id': playlist['id'],
                    }
                    count += 1
                    for token in tokenize(playlist['name'], lowercase=True):
                        word_counts[token] += 1
            break

def track_yielder(session, playlist):
    res = session.user_playlist_tracks(playlist['owner'], playlist['id'],
              fields='items(track(id, name, artists(name, id), duration_ms)),next')
    while res:
        for track in res['items']:
            if track['track']:
                yield track['track']
        tries = 3
        while tries > 0:
            try:
                res = session.next(res)
                if not res or  not res.get('items'):
                    raise StopIteration
                tries = 0
            except SpotifyException as e:
                if 400 <= e.http_status <= 499:
                    raise StopIteration
                tries -= 1
                time.sleep(1)
                if tries == 0:
                    raise e

from sqlite3 import Error
import os
import sqlite3

conn = None
def create_a_connection():
    try:
        if os.path.isfile('data/songs.db'): #if you made misateke erase a database
            os.remove('data/songs.db')
        conn = sqlite3.connect('data/songs.db')
        c = conn.cursor()
        c.execute('CREATE TABLE songs (id text primary key, name text, artist text)')
        c.execute('CREATE INDEX name_idx on songs(name)')
        print(sqlite3.version)
    except Error as err:
        print(err)

tracks_seen = set()

create_a_connection()

with open('data/playlists.ndjson', 'w') as fout_playlists:
    with open('data/songs_ids.txt', 'w') as fout_song_ids:
        for playlist in tqdm.tqdm(playlists.values()):
            fout_playlists.write(json.dumps(playlist) + '\n')
            track_ids = []
            for track in track_yielder(session, playlist):
                track_id = track['id']
                if not track_id:
                    continue
                if not track_id in tracks_seen:
                    c.execute("INSERT INTO songs VALUES (?, ?, ?)",
                              (track['id'], track['name'], track['artists'][0]['name']))
                track_ids.append(track_id)
            fout_song_ids.write(' '.join(track_ids) + '\n')
            conn.commit()
conn.commit()