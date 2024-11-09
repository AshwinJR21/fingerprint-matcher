from keras import models
import numpy as np
from PIL import Image
import cv2 as cv

def show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def SNN_process(image1, image2, threshold=0.8):
    model = models.load_model('SNN_model.h5')

    image1 = cv.imread(image1, cv.IMREAD_GRAYSCALE)
    image1 = cv.resize(image1, (90, 90))
    image1 = np.expand_dims(image1, axis=-1)

    image2 = cv.imread(image2, cv.IMREAD_GRAYSCALE)
    image2 = cv.resize(image2, (90, 90))
    image2 = np.expand_dims(image2, axis=-1)
    show('img1', image1)
    show('img2', image2)
    image1 = image1.reshape((1, 90, 90, 1)).astype(np.float32) / 255.
    image2 = image2.reshape((1, 90, 90, 1)).astype(np.float32) / 255.



    prediction = model.predict([image1, image2])

    match = True if prediction > threshold else False
    return prediction[0][0], match

