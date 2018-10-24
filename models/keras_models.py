from keras.models import Sequential
from keras.layers import Activation, BatchNormalization, Flatten, Dropout
from keras.layers import Dense, Conv1D, MaxPooling1D

def make_1d_nn_model(num_classes, num_input_feats):
    """ Defines a keras Sequential 1D NN model 
    
    Args: 
      num_classes - (int) number of classes to predict 
    Returns: 
      loads self.model as the defined model
    """
    model = Sequential()

    model.add(Flatten())
    model.add(Dense(units=256, activation='relu', input_shape=(num_input_feats, 1)))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    return model

def make_1d_cnn_model(num_classes, num_input_feats):
    """ Defines a keras Sequential 1D CNN model 
    
    Args: 
      num_classes - (int) number of classes to predict 
    Returns: 
      loads self.model as the defined model
    """
    model = Sequential()

    model.add(Conv1D(32, kernel_size=5,
              strides=1, activation='relu',
              input_shape=(num_input_feats, 1)))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=2, strides=2))

    model.add(Conv1D(64, 5, activation='relu'))     
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=2, strides=2))

    model.add(Conv1D(128, 5, activation='relu'))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=2, strides=2))

    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    return model
