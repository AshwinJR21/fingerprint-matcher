import os
import cv2 as cv
from PIL import Image
import io
import base64
import numpy as np
from flask import jsonify

def sift_process(image_file):
    imagee = Image.open(image_file)
    imagee_np = np.array(imagee)
    image_cv = cv.cvtColor(imagee_np, cv.COLOR_RGB2BGR)
    sample = image_cv
    #sample = cv.imread(r"D:\amrita\sem3\introduction to AI and ML\datasets\dataset_fingerprint\SOCOFing\Altered\Altered-Hard\184__M_Left_middle_finger_Obl.BMP")
    sample = cv.resize(sample, (100, 100))

    filename = None
    image = None
    keyPointsimg1, keyPointsimg2, matchPointsimg = None, None, None
    score_matched_percent = 0
    counter = 0
    for file in os.listdir(r"D:\amrita\sem3\introduction to AI and ML\datasets\dataset_fingerprint\SOCOFing\Real")[:1000]:
        print(file)
        if counter % 10 == 0:
            print(counter)
        counter += 1
        fingerprint_real_image = cv.imread(rf"D:\amrita\sem3\introduction to AI and ML\datasets\dataset_fingerprint\SOCOFing\Real\{file}")
        fingerprint_real_image = cv.resize(fingerprint_real_image, (100, 100))
        sift = cv.SIFT_create()
        keyPoints1, descriptors1 = sift.detectAndCompute(sample, None)
        keyPoints2, descriptors2 = sift.detectAndCompute(fingerprint_real_image, None)
        matches = cv.FlannBasedMatcher({'algorithm': 1, 'trees' : 10}, {}).knnMatch(descriptors1, descriptors2, k = 2)
        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)
        keypoints = len(keyPoints1) if len(keyPoints1) < len(keyPoints2) else len(keyPoints2)
        if (len(match_points) / keypoints) * 100 > score_matched_percent: 
            score_matched_percent = (len(match_points) / keypoints) * 100
            filename = file
            image = fingerprint_real_image
            keyPointsimg1, keyPointsimg2, matchPointsimg = keyPoints1, keyPoints2, match_points
    result = cv.drawMatches(sample, keyPointsimg1, image, keyPointsimg2, matchPointsimg, None)
    result = cv.resize(result, None, fx = 2, fy = 2)
    print(filename)
    print(score_matched_percent)
    #show("result", result)
     # Convert the processed image back to a format that can be sent (PIL)
    pil_image = Image.fromarray(result)
    # Convert processed image to bytes
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    # Encode the image in base64 to send back to the frontend
    encoded_img = base64.b64encode(img_byte_arr).decode('utf-8')
    # Send the processed image back to the frontend
    return jsonify({'processed_image': encoded_img,
                    'filename': filename,
                    'score': score_matched_percent})