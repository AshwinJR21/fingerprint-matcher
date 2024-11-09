from fingerprints import DATA_DIR, image1, image2, image3
import matplotlib.pyplot as plt
import cv2 as cv


median_blur = cv.medianBlur(image1, 3)
median_blur2 = cv.medianBlur(image2, 3)

