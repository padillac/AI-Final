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
        self.model.add(Dense(13, input_shape=(13,), activation='relu'))
        self.model.add(Dense(1, activation='softmax')) # Output layer

        self.model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy'])


    def trainModel(self, x_train, y_train):
        self.model.fit(x=x_train, y=y_train, batch_size=5, epochs=20, verbose=2, validation_split=0.1, shuffle=False)


    def predictPreferences(self, x_data):
        pass
