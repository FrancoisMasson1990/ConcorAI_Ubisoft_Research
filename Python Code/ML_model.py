#! /usr/bin/python
#--------------------------------#
# Model to train on yes/no detection
#--------------------------------#
# @FrancoisMasson

import os
import numpy
import pandas as pd
import shutil

import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from keras.callbacks import Callback
from keras.callbacks import EarlyStopping
from keras.utils.np_utils import to_categorical

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline

import matplotlib.pyplot as plt

### Load Data 

#df = pd.read_csv('Data/accel_x_final_dataset.csv')
df = pd.read_csv('Data_Save/Merge_Yes_data.csv')

dataset = df.values

X = dataset[:,0:40].astype(float) # sensor data
Y = dataset[:,40].astype(int) # labels

### Model NN

def create_model():
    # Define model
    global model
    model = Sequential()
    model.add(Dense(25, input_dim=40, activation='relu'))
    model.add(Dense(25, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(25, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


### Configure model callbacks including early stopping routine

class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        
loss_history = LossHistory()
early_stopping = EarlyStopping(monitor='val_acc', patience=20)

### Assemble classifier and train it

estimator = KerasClassifier(create_model, epochs=200, batch_size=30, verbose=False)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=15)
Y_test = to_categorical(Y_test)

results = estimator.fit(X_train, Y_train, callbacks=[loss_history, early_stopping], validation_data=(X_test, Y_test))

### Perform 10-fold cross-validation on validation data

kfold = KFold(n_splits=10, shuffle=True, random_state=5)
cv_results = cross_val_score(estimator, X_test, Y_test, cv=kfold)
print("Baseline on test data: %.2f%% (%.2f%%)" % (cv_results.mean()*100, cv_results.std()*100))

## If satisfied with Model :
# saving weights
#estimator.model.save_weights('model.h5', overwrite=True)
estimator.model.save('model_yes.h5', overwrite=True)

### Plot accuracy for train and validation data

#figsize = (15, 5)
#fig, ax = plt.subplots(figsize=figsize)
#ax.plot(results.history['val_acc'], linewidth=0.4, color="green")
#ax.plot(results.history['acc'], linewidth=0.4, color="red")
#plt.figure()
#plt.show()

"""
https://medium.com/tensorflow/train-on-google-colab-and-run-on-the-browser-a-case-study-8a45f9b1474e
https://colab.research.google.com/notebooks/welcome.ipynb#recent=true
https://medium.com/@aneeshpanoli/how-to-use-a-pre-trained-tensorflow-keras-models-with-unity-ml-agents-bee9933ce3c1
https://blog.goodaudience.com/tensorflow-unity-how-to-set-up-a-custom-tensorflow-graph-in-unity-d65cc1bd1ab1

"""