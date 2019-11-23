import sys
import os.path
import time
import math
from tqdm import tqdm #progress bars
import numpy as np
#from flask import Flask #allow webapp capabilities


#Allow local files to be imported
sys.path.insert(1, 'helpers/')
sys.path.insert(1, 'classes/')

from SongLoader import SongLoader #code that generates list of all tracks
from NeuralNet import NeuralNet #object that generates recommendations
from DataManager import DataManager #object that manages Spotify and NeuralNet data
#import FlaskFunctions as ff #functions that generate flask pages






def getBestPredictedSong(nn, dm):
    unknownSongData, indexTranslator = dm.getUnknownSongData()
    print("unknownSongData")
    print(unknownSongData.shape)
    predictions = nn.predictPreferences(unknownSongData)
    print("PREDICTIONS:-----")
    print(predictions.shape)
    print("max prediction:")
    maxIndex = np.argmax(predictions, axis=0)[0]
    print("index:", maxIndex)
    print(predictions[maxIndex])
    print(dm.getTrackData(indexTranslator[maxIndex])['name'])




def initializeDataManager():
    dm = DataManager()

    t1 = time.time()
    loader = SongLoader()
    dm.loadTrackData(loader.loadSongs())
    t2 = time.time()
    print("---- {} tracks loaded. {} hours, {} minutes and {} seconds".format(len(dm.trackData), math.floor((t2-t1)/3600), math.floor((t2-t1)/60), round((t2-t1)%60, 4)))

    return dm








def main():
    #Initialize DataManager
    dm = initializeDataManager()


    #Load/Create preference data
    if os.path.isfile('preference-data-cache'):
        dm.loadPreferencesFromFile('preference-data-cache')
    else:
        print("No training data found. Creating some known training data")

        for id, t in dm.getTrackIterator():
            print("{}, {} -- Listen: {}".format(t['name'], t['artists'][0]['name'], t['external_urls']['spotify']))
            designation = input("Like? 1 or 0 (q to stop deciding): ")
            if designation == '':
                continue
            if designation == 'q':
                break
            if int(designation) == 1:
                print("liked")
            if int(designation) == 0:
                print("disliked")
            dm.updateKnownData(id, int(designation))

        print("Done creating training data")
        dm.savePreferencesToFile('preference-data-cache')

    print("Generating 2,000 random preferences")
    dm.generateRandomPreferences(2000)


    print("----------TRAINING NEURAL NET-----------")

    nn = NeuralNet()
    nn.buildModel()
    #nn.plotModel()
    #nn.displayModel()
    nn.trainModel(dm.x_known, dm.y_known)


    print("-------------NEURAL NET RECOMMENDATIONS-----------")

    #for id, t in dm.getTrackIterator():
    #    print("{}, {} --".format(t['name'], t['artists'][0]['name']))
    #    nn.predictPreferences(dm.getTrackNeuralNetArray(id))

    getBestPredictedSong(nn, dm)





if __name__ == '__main__':
    main()
