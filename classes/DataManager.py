import numpy as np
import pickle #storing objects in files
import random #allows generation of track iterators in random order
from tqdm import tqdm #progress bars

# This class manages all song data and provides a simple API for updating training sets,
# and prepping data for neural net predictions
class DataManager:
    x_known = None
    y_known = None
    known_ids = []
    trackData = {}

    def __init__(self):
        self.x_known = np.empty((0,13))
        self.y_known = np.empty((0,2), int)




    def loadTrackData(self, tracks):
        for t in tracks:
            self.trackData[t['id']] = t

    def getTrackIterator(self):
        items = list(self.trackData.items())
        random.shuffle(items)
        return items


    def getTrackData(self, trackID):
        return self.trackData[trackID]

    def getTrackNeuralNetArray(self, trackID):
        af = self.trackData[trackID]['audio_features']
        if af is None:
            return [0,0,0,0,0,0,0,0,0,0,0,0,0]
        key = (af['key'])/(11)
        loudness = (af['loudness'] + 60)/(60)
        tempo = (af['tempo'])/(250)
        time_signature = (af['time_signature'])/(8)
        duration_ms = (af['duration_ms']-20000)/(340000)
        return np.array([af['danceability'], af['energy'], key, loudness, af['mode'], af['speechiness'], af['acousticness'], af['instrumentalness'], af['liveness'], af['valence'], tempo, duration_ms, time_signature])


    def updateKnownData(self, trackID, preference):
        if preference not in [0,1]:
            return
        newRowData = self.getTrackNeuralNetArray(trackID)
        self.x_known = np.append(self.x_known, [newRowData], axis=0)
        self.y_known = np.append(self.y_known, [[preference, 1-preference]], axis=0)
        self.known_ids.append(trackID)


    def getUnknownSongData(self):
        unknownSongData = np.empty((0,13))
        indexTranslator = {}
        print("compiling unknown song data into numpy array")
        for id, t in tqdm(self.getTrackIterator()):
            if t['id'] in self.known_ids:
                continue
            nnd = self.getTrackNeuralNetArray(id)
            unknownSongData = np.append(unknownSongData, [nnd], axis=0)
            indexTranslator[len(unknownSongData)-1] = id

        return unknownSongData, indexTranslator






    def generateRandomPreferences(self, n=500):
        count = 0
        for id, t in self.getTrackIterator():
            self.updateKnownData(id, random.randint(0,1))
            count += 1
            if count == n:
                return




    def savePreferencesToFile(self, path):
        with open(path, 'wb') as dataFile:
            pickle.dump((self.x_known, self.y_known), dataFile)
        print("saved preference data to file")

    def loadPreferencesFromFile(self, path):
        with open(path, 'rb') as dataFile:
            data = pickle.load(dataFile)
        self.x_known = data[0]
        self.y_known = data[1]
        print("preference data loaded from file")







#FUTURE: make this class specific to each user? possibly save known data to file to recover user preferences.
    # Would this mean I also need to have separate neural nets for each user?
