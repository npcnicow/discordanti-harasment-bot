#IMPORT
from keras.models import load_model
import time
from keras.preprocessing import text
import os

modelPath = '.\\modelTrained\\model.hdf5'
#Chargement du modele
print("\nChargement du modèle...")
model = load_model(modelPath)



def predict(inputText):
    maxWord = 10000
    if True :
        os.system('cls')
        # Recuperer le texte à tester
        

        start = time.time()

        print("\nTokenization du texte...")
        # Transforme le text vers une matrice de mot et permet de lui donnée un indice
        tokenize = text.Tokenizer(num_words=maxWord, char_level=False)
        tokenize.fit_on_texts(inputText)
        word = tokenize.texts_to_matrix(inputText)

        print("\nPrediction du texte...")
        prediction = model.predict(word)[0]
        #predictionWithLabel = text_labels[np.argmax(prediction)]
        end = time.time()
        print("\nProbabilites (temps : {0:.2f}secs)".format(end-start))
        print("\t- Non harcelement : {0:.2f}%".format(prediction[0]*100.))
        print("\t- Harcelement : {0:.2f}%".format(prediction[1]*100.))

        if prediction[1]*100 > 50 :
            return 1
        else:
            return 0
