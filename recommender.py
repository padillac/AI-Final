import sys
import getopt #allows command line arguments
import os.path
import time
import math
from tqdm import tqdm, trange #progress bars
import numpy as np
#from flask import Flask #allow webapp capabilities


#Allow local files to be imported
sys.path.insert(1, 'helpers/')
sys.path.insert(1, 'classes/')

from Functions import * #get functions for command line interface
from SongLoader import SongLoader #code that generates list of all tracks
from NeuralNet import NeuralNet #object that generates recommendations
from DataManager import DataManager #object that manages Spotify and NeuralNet data
from HiddenPrints import HiddenPrints #stifle built-in print statements
#import FlaskFunctions as ff #functions that generate flask pages






def main():
    #evaluate arguments
    PREFERENCE_DATA_PATH = None
    RAND_DATA_NUMBER = 0
    VERBOSE = False
    unixOptions = "hr:vp:"
    gnuOptions = ["help", "random=", "verbose", "preference="]
    try:
        arguments, values = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        helpmsg = "try 'python3 recommender.py -h' or 'python3 recommender.py --help' for help"
        print(str(err))
        sys.exit(2)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print ("usage:\n\tpython3 recommender.py -p | --preference_file file_path [-h|--help] [-v|--verbose] [-r|--random n]\n\nOptions:\n\t-p | --preference_file\tPath to preference data file. if one exists, it will be loaded and used to train the neural net. If it does not exist, it will be created to save your preference data.\n\t-h | --help\tDisplay this text\n\t-v | --verbose\tDisplay verbose neural net training information\n\t-r | --random n\tGenerate random training data of size n. If training data file exists this will be ignored. Usually results in recommendations for audiobooks or white noise.")
            exit()
        elif currentArgument in ("-v", "--verbose"):
            print("enabling verbose mode")
            VERBOSE = True
        elif currentArgument in ("-r", "--random"):
            RAND_DATA_NUMBER = currentValue
        elif currentArgument in ("-p", "--preference_file"):
            PREFERENCE_DATA_PATH = currentValue

    if PREFERENCE_DATA_PATH is None:
        print("You must specify a preference data file name.\nUse 'python3 recommender.py -h' for help.")
        sys.exit(2)

    #Initialize DataManager
    dm = initializeDataManager()


    #Load/Create preference data
    if os.path.isfile(PREFERENCE_DATA_PATH):
        dm.loadPreferencesFromFile(PREFERENCE_DATA_PATH)
        print("---- {} classified songs loaded.".format(len(dm.y_known)))
    elif RAND_DATA_NUMBER:
        print("Generating {} random preferences".format(RAND_DATA_NUMBER))
        dm.generateRandomPreferences(RAND_DATA_NUMBER)

    else:
        print("\nNo training data found. Start listening to get personalized recommendations!")
        print("Here are some random songs from the database. Take a listen, and enter '1' to indicate that you like the song, and '0' to indicate that you don't.")
        print("Type 'size' to check how many songs you have classified.")
        print("Once you have selected a few songs to start with, type 'train' to train the neural net and start listening to songs it thinks you'll like.")

        for id, t in dm.getTrackIterator():
            print("\n{} by {}\n-- Listen: {}".format(t['name'], t['artists'][0]['name'], t['external_urls']['spotify']))
            i = input(">>> ")
            if i.strip() == "exit":
                exit()
            elif i.strip() == "train":
                if len(dm.y_known) == 0:
                    print("\nYou must like or dislike at least one song.")
                    continue
                print("\nbuilding the neural net and training with your new preferences")
                break
            elif i.strip() == "size":
                print("\nYou have classified {} songs.".format(len(dm.y_known)))
            elif i.strip() == "1":
                dm.updateKnownData(id, 1)
            elif i.strip() == "0":
                dm.updateKnownData(id, 0)
            else:
                print("\ninvalid input, please try again")






    print("----------BUILDING NEURAL NET-----------")
    print("----IGNORE KERAS/TENSORFLOW ERRORS THAT DISPLAY ON THE FIRST BUILD----")

    nn = NeuralNet()
    nn.buildModel()
    #nn.plotModel()
    #nn.displayModel()
    if VERBOSE:
        print("training neural net")
        nn.trainModel(dm.x_known, dm.y_known)
    else:
        with HiddenPrints():
            nn.trainModel(dm.x_known, dm.y_known)



    print("--------------DONE-------------")



    #Initialize "radio" mode
    outOfSongs = False
    songIndex = 0
    recs = getTopSongs(nn, dm)
    if not recs:
        outOfSongs = True

    print("\n\nYou are now in radio mode!\n------------------\nListen to songs the neural net has picked for you, and tell it if you liked them!")
    print("Enter '1' to like, '0' to dislike, 'size' to check how many songs you've classified, 'train' to retrain the neural net with your new preferences, and 'exit' to save your preferences to file and quit")

    while not outOfSongs:
        t = recs[songIndex]
        print("\n{}% match: {} by {}\n-- Listen: {}".format(t['percent_match'], t['name'], t['artists'][0]['name'], t['external_urls']['spotify']))
        i = input(">>> ")
        if i.strip() == "exit":
            saveAndQuit(dm, PREFERENCE_DATA_PATH)
        elif i.strip() == "train":
            print("\ntraining the neural net on your new preferences")
            if VERBOSE:
                nn.trainModel(dm.x_known, dm.y_known)
            else:
                with HiddenPrints():
                    nn.trainModel(dm.x_known, dm.y_known)
            recs = getTopSongs(nn, dm)
            songIndex = 0
            if not recs:
                outOfSongs = True
                continue
        elif i.strip() == "size":
            print("\nYou have classified {} songs.".format(len(dm.y_known)))
        elif i.strip() == "1":
            dm.updateKnownData(t['id'], 1)
            songIndex += 1
        elif i.strip() == "0":
            dm.updateKnownData(t['id'], 0)
            songIndex += 1
        else:
            print("\ninvalid input, please try again")

    print("\n\nYou have somehow categorized every song in the local database! (if you created random preferences, maybe the number was too big)\nTo get more songs, add more countries or increase the parameters in SongLoader, change the name of the song-data-cache file (or delete it) and restart the program. Your preferences will be saved now.")
    saveAndQuit(dm, PREFERENCE_DATA_PATH)







if __name__ == '__main__':
    main()
