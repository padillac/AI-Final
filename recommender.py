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
    print("----Tracks loaded. {}".format(t2-t1))


    for track in tracks:
        print(track)
        time.sleep(2)







if __name__ == '__main__':
    main()
