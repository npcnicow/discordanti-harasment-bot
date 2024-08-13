#IMPORT
import pandas as pd
import keras
from sklearn.utils import shuffle
from keras.callbacks import CSVLogger
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing import text
from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras import utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout


'''
Permet d'attribuer l'allocation dynamique de mémoire pour éviter les depassements
'''
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

# Lecture de notre dataset
data = pd.read_csv('.\\dataset\\data.txt', sep=',', names=["text", "result"])


# On melange les donnees
data = shuffle(data)


# On verifie que le dataset est équilibré et que les classes soient bien conformes
print('DIMENSION DU DATASET')
print(data.shape)

print('EQUILIBRE DU DATASET')
print(data['result'].value_counts())


# Definition des callbacks
early = EarlyStopping(monitor='val_loss', min_delta=0, patience=2, verbose=0, mode='auto')
check = ModelCheckpoint('.\\modelTrained\\model.hdf5', monitor='val_loss', verbose=0,save_best_only=True, save_weights_only=False, mode='auto')
csvLogger = CSVLogger('.\\metrics\\log.csv', append=False, separator=',')


# Definition des jeux de train et test
trainSize = int(len(data) * .8)
print ("Train taille: %d" % trainSize)
print ("Test taille: %d" % (len(data) - trainSize))

trainText = data['text'][:trainSize]
trainResult = data['result'][:trainSize]

testText = data['text'][trainSize:]
testResult = data['result'][trainSize:]

# Fix des hyper parametres
batch_size = 256
epoch = 100
maxWords = 1000

# Transforme le text vers une matrice de mot et permet de lui donnée un indice
tokenize = text.Tokenizer(num_words=maxWords, char_level=False)
tokenize.fit_on_texts(trainText)
xTrain = tokenize.texts_to_matrix(trainText)
xTest = tokenize.texts_to_matrix(testText)


#Défini les labels des prédictions
encoder = LabelEncoder()
encoder.fit(trainResult)
yTrain = encoder.transform(trainResult)
yTest = encoder.transform(testResult)
numClasses = np.max(yTrain) + 1

yTest = utils.to_categorical(yTest, numClasses)
yTrain = utils.to_categorical(yTrain, numClasses)


# Shape de nos donnees avant entrainement
print('xTrain shape:', xTrain.shape)
print('xTest shape:', xTest.shape)
print('yTrain shape:', yTrain.shape)
print('yTest shape:', yTest.shape)




# Definition de notre modele
model = Sequential()
model.add(Dense(512, input_shape=(maxWords,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(numClasses))
model.add(Activation('softmax'))


# Compilation du modele
model.compile(loss='categorical_crossentropy',optimizer=keras.optimizers.Adamax(lr=0.001, beta_1=0.9, beta_2=0.999, decay=0.0),metrics=['accuracy'])


# Entrainement du modele
train =  model.fit(xTrain, yTrain, epochs=epoch, callbacks = [csvLogger, early, check], batch_size=batch_size, validation_data=(xTest,yTest))
