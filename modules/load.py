from modules.image2minst import *
from keras.models import model_from_json
from matplotlib import pyplot as plt
from matplotlib import image as pltImage
import numpy as np


class Model:
    def __init__(self):
        with open("models/model.json") as json_model:
            self.model = model_from_json(json_model.read())
            json_model.close()

        self.model.load_weights("models/model.weights")
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def Predict(self, image):
        array = [imageprepare(image)]
        imageArray = [[0 for d in range(28)] for y in range(28)]
        k = 0
        for i in range(28):
            for j in range(28):
                imageArray[i][j] = array[0][k]
                k = k + 1

        imageArray = np.array(imageArray)
        imageArray = imageArray.reshape(1, 28, 28, 1)

        pltImage.imsave("images/current.png", imageArray.reshape(28,28))

        scores = self.model.predict(np.array(imageArray))

        number = 0
        bestScore = -1
        prediction = -1
        for score in scores[0]:
            if score > bestScore:
                bestScore = score
                prediction = number

            number += 1

        return prediction, scores[0]
