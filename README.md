# Music Recommendation App Model Part 

- We can try to build model on top the dusty, external drive with mine MP3 collection on it and relying on the tags on those songs. But a lot of those tags may be somewhat random or missing, so it’s best to get started with a training set from a scientific institution that is nicely labeled:
    
  ```
    wget http://opihi.cs.uvic.ca/sound/genres.tar.gz 
    tar xzf genres.tar.gz
    ```
  
- 100 clips per genre, each 29 seconds long. We could try to feed the raw sound frames directly into the network and maybe an LSTM would pick up something, but there are better ways of preprocessing sounds. 
- Sound is really sound waves, but we don’t hear waves. Instead, we hear tones of a cer‐ tain frequency.
So a good way to make our network behave more like our hearing works is to convert sound into blocks of spectrograms; each sample will be represented by a series of audio freqencies and their respective intensities.

- Let's have look at quick analysis further on our data:

     ![Screenshot](/Users/eneskaranfil/Desktop/class.png)
- Chart above indicates density of classical music of genre.