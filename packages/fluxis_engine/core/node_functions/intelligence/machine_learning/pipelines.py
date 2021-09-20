from sklearn import preprocessing
import numpy as np

DEFAULT_PIPELINE = [('scaler', preprocessing.RobustScaler()), ]
