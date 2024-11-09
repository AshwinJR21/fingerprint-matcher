from flask import Flask, request, jsonify
from flask_cors import CORS
from sift import sift_process
from SNNModel import SNN_process
from featureModel import featureModel_process


# def show(name, img):
#     cv.imshow(name, img)
#     cv.waitKey(0)
#     cv.destroyAllWindows()


app = Flask(__name__)
CORS(app)
@app.route('/sift-upload', methods=['POST'])
def upload_image_sift():
    image_file = request.files.get('image')

    if image_file:
        return sift_process(image_file)
    else:
        return jsonify({'error': 'No image uploaded'}), 400
    
@app.route('/snn-upload', methods=['POST'])
def upload_image_snn():
    image1 = request.files.get('image1')
    image2 = request.files.get('image2')
    if image1 and image2:
        return SNN_process(image1, image2)
    else:
        return jsonify({'error': 'No image uploaded'}), 400
    
@app.route('/snnplus-upload', methods=['POST'])
def upload_image_snnplus():
    image = request.files.get('image')
    if image:
        return featureModel_process(image)
    else:
        return jsonify({'error': 'No image uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)
