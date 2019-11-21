import sys
import os.path
import time
import math
from tqdm import tqdm #progress bars
import numpy as np

#Allow local files to be imported
sys.path.insert(1, 'helpers/')
sys.path.insert(1, 'classes/')

from SongLoader import SongLoader #code that generates list of all tracks
from NeuralNet import NeuralNet #object that generates recommendations
from DataManager import DataManager #object that manages Spotify and NeuralNet data






def main():
    #Initialize DataManager
    dm = DataManager()


    t1 = time.time()
    loader = SongLoader()
    dm.loadTrackData(loader.loadSongs())
    t2 = time.time()
    print("----Tracks loaded. {} hours, {} minutes and {} seconds".format(math.floor((t2-t1)/3600), math.floor((t2-t1)/60), round((t2-t1)%60, 4)))





    if os.path.isfile('preference-data-cache'):
        dm.loadPreferencesFromFile('preference-data-cache')
    else:
        print("No training data found. Creating some known training data")

        for t in dm.getTrackIterator():
            print("{}, {} -- Listen: {}".format(t['name'], t['artists'][0]['name'], t['external_urls']['spotify']))
            designation = input("Like? 1 or 0 (q to stop deciding): ")
            if designation == 'q':
                break
            if int(designation) == 1:
                print("liked")
            if int(designation) == 0:
                print("disliked")
            dm.updateKnownData(t['id'], int(designation))

        print("Done creating training data")
        dm.savePreferencesToFile('preference-data-cache')


    print("----------TRAINING NEURAL NET-----------")

    nn = NeuralNet()
    nn.buildModel()
    nn.trainModel(dm.x_known, dm.y_known)












if __name__ == '__main__':
    main()
