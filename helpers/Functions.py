#Functions used by recommender.py main() function

import sys
import getopt #allows command line arguments
import os.path
import time
import math
from tqdm import tqdm, trange #progress bars
import numpy as np
#from flask import Flask #allow webapp capabilities

#Allow local files to be imported
import sys
sys.path.insert(1, '../classes/')

from SongLoader import SongLoader #code that generates list of all tracks
from NeuralNet import NeuralNet #object that generates recommendations
from DataManager import DataManager #object that manages Spotify and NeuralNet data
from HiddenPrints import HiddenPrints #stifle built-in print statements
#import FlaskFunctions as ff #functions that generate flask pages



def getTopSongs(nn, dm):
    print("getting data on new songs from local database")
    unknownSongData, indexTranslator = dm.getUnknownSongData()
    if len(unknownSongData) == 0:
        return False
    print("using neural net to find personalized matches")
    predictions = nn.predictPreferences(unknownSongData)
    sortedPredictions = predictions[predictions[:,0].argsort()[::-1]]
    recs = []
    print("collecting data on top 100 matches")
    for i in trange(100):
        index = np.where(predictions == sortedPredictions[i])[0][0]
        trackID = indexTranslator[index]
        trackData = dm.getTrackData(trackID)
        trackData['percent_match'] = round(sortedPredictions[i][0]*100, 1)
        recs.append(trackData)
    return recs




def initializeDataManager():
    dm = DataManager()

    t1 = time.time()
    loader = SongLoader()
    dm.loadTrackData(loader.loadSongs())
    t2 = time.time()
    print("---- {} tracks loaded. {} hours, {} minutes and {} seconds".format(len(dm.trackData), math.floor((t2-t1)/3600), math.floor((t2-t1)/60), round((t2-t1)%60, 4)))

    return dm



def saveAndQuit(dm, path):
    print("saving preferences to file.")
    dm.savePreferencesToFile(path)
    print("exiting")
    exit()
