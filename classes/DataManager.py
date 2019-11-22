import numpy as np
import pickle #storing objects in files

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
        return self.trackData.values()


    def getTrackNeuralNetArray(self, trackID):
        af = self.trackData[trackID]['audio_features']
        return np.array([af['danceability'], af['energy'], af['key'], af['loudness'], af['mode'], af['speechiness'], af['acousticness'], af['instrumentalness'], af['liveness'], af['valence'], af['tempo'], af['duration_ms'], af['time_signature']])


    def updateKnownData(self, trackID, preference):
        if preference not in [0,1]:
            return
        newRowData = self.getTrackNeuralNetArray(trackID)
        self.x_known = np.append(self.x_known, [newRowData], axis=0)
        self.y_known = np.append(self.y_known, [[preference, 1-preference]], axis=0)
        self.known_ids.append(trackID)


    def getUnknownSongData(self):
        unknownSongData = np.empty((0,13))
        for t in self.getTrackIterator():
            if t['id'] in self.known_ids:
                continue
            nnd = self.getTrackNeuralNetArray(t['id'])
            unknownSongData = np.append(unknownSongData, [nnd], axis=0)

        return unknownSongData




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
