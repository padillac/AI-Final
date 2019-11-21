from HiddenPrints import HiddenPrints #stifle built-in print statements
with HiddenPrints():
    from keras.models import Sequential
    from keras.layers import Dense, Activation



class NeuralNet:

    model = None

    def __init__(self):
        pass

    def buildModel(self):
        self.model = Sequential()
