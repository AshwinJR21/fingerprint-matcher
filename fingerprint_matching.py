from flask import Flask, request, jsonify
from flask_cors import CORS
from sift import sift_process


# def show(name, img):
#     cv.imshow(name, img)
#     cv.waitKey(0)
#     cv.destroyAllWindows()


app = Flask(__name__)
CORS(app)
@app.route('/upload', methods=['POST'])
def upload_image():
    image_file = request.files.get('image')

    if image_file:
        return sift_process(image_file)
    else:
        return jsonify({'error': 'No image uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)
