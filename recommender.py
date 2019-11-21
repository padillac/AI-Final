import sys
import time

#Allow local files to be imported
sys.path.insert(1, 'helpers/')
sys.path.insert(1, 'functions/')

from SongLoader import SongLoader #code that generates list of all tracks
from tqdm import tqdm #progress bars






def main():
    t1 = time.time()
    loader = SongLoader()
    tracks = loader.loadSongs()
    t2 = time.time()
    print("----Tracks loaded. {} seconds".format(t2-t1))



    print(tracks[0])

    #for track in tracks:
        #if track is not None:
            #print("{}, {}".format(track['name'], track['artists'][0]['name']))







if __name__ == '__main__':
    main()
