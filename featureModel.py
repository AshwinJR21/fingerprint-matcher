from keras import models
import numpy as np
from PIL import Image
import cv2 as cv
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import io
import base64
from flask import jsonify

_path = "D:/amrita/sem3/introduction to AI and ML/datasets/dataset_fingerprint/numpy_dataset/"
x_real = np.load(rf"{_path}/xReal.npz")['arr_0']
y_real = np.load(rf"{_path}/yReal.npy")
model = models.load_model('featureModel.h5')
flat_embed = model.predict(x_real).reshape(6000, -1)

def showMatch(inputImg, idx, percent):
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.title('Input image:')
    plt.imshow(inputImg.squeeze(), cmap='gray')
    plt.subplot(1, 2, 2)
    plt.title('                     Matched Image: %.02f, %s' % (percent, y_real[idx]))
    plt.imshow(x_real[idx].squeeze(), cmap='gray')

    # Save plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='JPEG', bbox_inches='tight', pad_inches=0)
    buf.seek(0)  # Go back to the beginning of the buffer
    plt.close()
    ret = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return jsonify({'processed_image': ret,
                    'score': percent})

def featureModel_process(image):

    image = Image.open(image).convert('L')
    image = cv.resize(np.array(image), (90, 90))
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32) / 255.

    input_embed = model.predict(image)
    input_flat_embed = input_embed.flatten()

    similarity_scores = cosine_similarity(input_flat_embed.reshape(1, -1), flat_embed)
    max_sim_index = np.argmax(similarity_scores)
    max_sim_score = similarity_scores[0, max_sim_index]
    percent = ((max_sim_score+1)/2) * 100
    if percent <= 99.2: print('match is not accurate. Fingerprint may not be present in the database')
    return showMatch(image, max_sim_index, percent)

