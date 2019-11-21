import sys

#Allow local files to be imported
sys.path.insert(1, 'helpers/')
sys.path.insert(1, 'functions/')

from SongLoader import SongLoader #code that generates list of all tracks
from tqdm import tqdm #progress bars





loader = SongLoader()
tracks = loader.loadSongs()
print(tracks[0])
