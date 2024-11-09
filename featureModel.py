from keras import models

def featureModel_process(image):
    model = models.load_model('featureModel.h5')
    