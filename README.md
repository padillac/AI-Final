# Spotify Song Recommender

This program allows you to create your own personalized radio stations based on your preferences. It uses the spotify API to gather metadata and audio data on large amounts of songs, and uses a Keras neural network to find patterns in songs that you classify by either "liking" or "disliking".

After you tell it a few songs that you like, the neural network quickly picks up on patterns in genre and general style and will recommend similar songs to you. You can continuously train the neural network as you browse the songs that it selects for you, which allows your custom station to get better and better the more you interact with it.

You also have the ability to name and save your preferences files, and choose one to load each time you start the program. This allows you to have multiple "stations" that are independently trained. Think of this as training different stations for different genres or moods for best results.


## Installation:

1. Clone the repository
```bash
git clone https://github.com/padillac/AI-Final.git
```

2. Run setup.py to install all dependencies via pip
```bash
python3 setup.py
```

3. If you have any song data files or preference files, move them to the root directory, next to recommender.py. The song data file should be named 'SONG_DATA' and any preference file should be a '.p' file (to work with the gitignore)

## Quick Start

1. Run the program with a new preferences file and it will automatically load Spotify data and help get you started.

```bash
python3 recommender.py -p newpreferences.p
```
 (Replace newpreferences.p with the name of an existing .p file to load those preferences and train the neural net on them immediately)

 2. Run the program with random preferences to get started with a larger dataset and see what happens!

 ```bash
python3 recommender.py -p random.p -r 500 -v
 ```
 (change 500 to the number of random data points you want to create. -v option enables verbose mode)



## Theory

The neural net currently evaluates songs by making a categorical classification between songs that you like, and songs that you don't. The inputs considered are normalized vectors representing danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration, and time signature.

These data are all taken directly from the Spotify API for each song. See https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/ for a reference on what these features mean.
