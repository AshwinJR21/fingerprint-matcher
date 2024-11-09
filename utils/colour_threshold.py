from matplotlib import pyplot as plt
import cv2 as cv

def show_image_thresholds(img):
    ret, thres1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
    ret, thres2 = cv.threshold(img, 127, 255, cv.THRESH_OTSU)
    ret, thres3 = cv.threshold(img, 127, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    ret, thres4 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    ret, thres5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)

    titles = ['Original image', 'Binary Inverse', 'OTSU', 'Binary|OTSU', 'Binary', 'ToZero Inverse']
    images = [img, thres1, thres2, thres3, thres4, thres5]

    for i in range(6):
        plt.subplot(2, 3, i+1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    
    plt.show()
    
    return thres2
