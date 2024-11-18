import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras import models
import numpy as np
from PIL import Image
import cv2 as cv
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib import use
import matplotlib.pyplot as plt
use('Agg')
import io
import base64
from flask import jsonify
import time
from pandas import read_excel

_path = "D:/amrita/sem3/introduction to AI and ML/datasets/dataset_fingerprint/numpy_dataset/"
x_real = np.load(rf"{_path}/xReal.npz")['arr_0']
y_real = np.load(rf"{_path}/yReal.npy")
data = read_excel(r"D:\amrita\sem3\introduction to AI and ML\datasets\fingerprint_fake_dataset.xlsx")
model = models.load_model('featureModel.h5', compile=False)
flat_embed = model.predict(x_real).reshape(6000, -1)

def return_filename(label):
    id = label[0]
    gender = 'F' if label[1] else 'M'
    lr = 'Right' if label[2] else 'Left'
    if label[3] == 0:
        finger = 'thumb'
    elif label[3] == 1:
        finger = 'index'
    elif label[3] == 2:
        finger = 'middle'
    elif label[3] == 3:
        finger = 'ring'
    else:
        finger = 'little'
    return f"{id}__{gender}_{lr}_{finger}_finger.BMP"

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
    index = np.where(data['image path'] == rf"D:\amrita\sem3\introduction to AI and ML\datasets\dataset_fingerprint\SOCOFing\Real\{return_filename(y_real[idx])}")[0][0]
    row = data.iloc[index, :]
    return jsonify({'processed_image': ret,
                    'score': percent,
                    'name' : str(row['name']),
                    'gender' : str(row['gender']),
                    'lr' : str(row['lr']),
                    'finger' : str(row['finger']),
                    'dob' : str(row['dob']).split(' ')[0],
                    'country' : str(row['country']),
                    'phone' : str(row['phone']),
                    'address' : str(row['address'])})

def featureModel_process(image):
    ts = time.time()
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
    te = time.time()
    print("time taken for feature comparison", round(te - ts, 4), " s")
    return showMatch(image, max_sim_index, percent)

