# Music Recommendation App Model Part 

- We can try to build model on top the dusty, external drive with mine MP3 collection on it and relying on the tags on those songs. But a lot of those tags may be somewhat random or missing, so it’s best to get started with a training set from a scientific institution that is nicely labeled:
    
    ```
    wget http://opihi.cs.uvic.ca/sound/genres.tar.gz 
    tar xzf genres.tar.gz
    ```
[!Hint]  Also, check kaggle for dataset. That maybe useful.

- 100 clips per genre, each 27 seconds long. We could try to feed the raw sound frames directly into the network and maybe an LSTM would pick up something, but there are better ways of preprocessing sounds. 

- Chart above indicates density of classical music of genre.
