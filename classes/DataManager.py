import numpy as np


# This class manages all song data and provides a simple API for updating training sets,
# and prepping data for neural net predictions
class DataManager:
    x_known = None
    y_known = None

    x_unknown = None

    trackData = None

    def __init__(self):
        self.x_known = np.empty((0,13))
        self.y_known = np.empty((0,1), int)
