import os
from tinytag import TinyTag, TinyTagException
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
from keras.models import load_model
import librosa
from collections import Counter
import multiprocessing
from tqdm import tqdm
from keras.models import Model
import numpy as np
import sounddevice as sd


root = "/Users/eneskaranfil/songs/"
mp3s = []
for root, subdirs, files in os.walk(root):
    for fn in files:
        if fn.endswith('.mp3'):
            mp3s.append(os.path.join(root, fn))

print(mp3s)
print(len(mp3s))

TO_SKIP = {'Podcast', 'Books & Spoken'}

def process_mp3(path):
    try:
        tag = TinyTag.get(path)
    except TinyTagException:
        print('error')
        return None
    signal, sr = librosa.load(path, res_type='kaiser_fast', offset=30, duration=27)
    print(signal)
    print(sr)
    try:
        melspec = librosa.feature.melspectrogram(signal, sr=sr).T[:1280,]
    except ValueError:
        return None
    return {'path': path,
            'melspecs': np.asarray(melspec),
            'tag': tag}

songs = [process_mp3(path) for path in tqdm(mp3s[:1000])]
songs = [song for song in songs if song]

print(songs)


inputs = []
for song in songs:
    inputs.extend(song['melspecs'])
inputs = np.array(inputs)

cnn_model = load_model('model/song_classify.h5')
vectorize_model = Model(inputs=cnn_model.input, outputs=cnn_model.layers[-4].output)
vectors = vectorize_model.predict(inputs)


nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(vectors)

def most_similar_songs(song_idx):
    distances, indices = nbrs.kneighbors(vectors[song_idx * 10: song_idx * 10 + 10])
    c = Counter()
    for row in indices:
        for idx in row[1:]:
            c[idx // 10] += 1
    return c.most_common()


song_idx = 7
print(songs[song_idx]['path'])

print('---')
for idx, score in most_similar_songs(song_idx)[:5]:
    print(songs[idx]['path'], score)
print('')
