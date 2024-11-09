from keras import models
import numpy as np
from PIL import Image
import cv2 as cv
import matplotlib.pyplot as plt
from flask import jsonify
import io
import base64

def show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def result_return(image1, image2, score, match, prediction):
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 3, 1)
    plt.title('Input image:')
    plt.imshow(image1.squeeze(), cmap='gray')
    plt.subplot(1, 3, 2)
    plt.title('                   Matched Image: %.02f, %s' % (score, match))
    plt.imshow(image2.squeeze(), cmap='gray')
    # Save plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='JPEG', bbox_inches='tight', pad_inches=0)
    buf.seek(0)  # Go back to the beginning of the buffer
    plt.close()
    ret = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return jsonify({'processed_image': ret,
                    'match': match,
                    'score': float(prediction[0][0])})

def SNN_process(image1, image2, threshold=0.8):
    model = models.load_model('SNN_model.h5')

    image1 = Image.open(image1).convert('L')
    image1 = cv.resize(np.array(image1), (90, 90))
    image1 = np.expand_dims(image1, axis=0)

    image2 = Image.open(image2).convert('L')
    image2 = cv.resize(np.array(image2), (90, 90))
    image2 = np.expand_dims(image2, axis=0)
    # show('img1', image1)
    # show('img2', image2)
    image1 = image1.astype(np.float32) / 255.
    image2 = image2.astype(np.float32) / 255.

    prediction = model.predict([image1, image2])

    match = True if prediction > threshold else False

    return result_return(image1, image2, prediction[0][0], match, prediction)
