import numpy as np
from HiddenPrints import HiddenErrors #stifle built-in print statements
with HiddenErrors():
    from keras.models import Sequential
    from keras.layers import Dense, Activation, Dropout
    from keras.optimizers import RMSprop
    from keras.utils import plot_model



class NeuralNet:

    model = None

    def __init__(self):
        pass

    def buildModel(self):
        self.model = Sequential()
        self.model.add(Dense(13, input_shape=(13,), activation='relu'))
        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dense(2, activation='softmax')) # Output layer

        #opt = RMSprop(learning_rate=0.0001, decay=1e-6)
        self.model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])


    def displayModel(self):
        self.model.summary()

    def plotModel(self, path='model.png'):
        plot_model(self.model, show_shapes=True, to_file=path)



    def trainModel(self, x_train, y_train):
        with HiddenErrors():
            self.model.fit(x=x_train, y=y_train, batch_size=32, epochs=25, verbose=2, validation_split=0.1, shuffle=True)


    def predictPreferences(self, x_data):
        return self.model.predict(x_data)









#
