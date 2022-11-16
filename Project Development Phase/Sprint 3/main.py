import os
import test1
import cv2
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "fileUpload"


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods= ["POST"])
def upload():
    f = request.files['cheque']
    validExt = ['png', 'jpg', 'jpeg', 'tif', 'eps', 'gif']
    extension = f.filename.split('.')[1]
    if extension not in validExt:
        return "Not a valid extension"

    fname = secure_filename(str(len(os.listdir('fileUpload')))) + "." + extension
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
    img = cv2.imread("fileUpload\\" + fname)
    res = test1.crop(img, fname)
    print(res)
    return render_template("results.html")


if __name__ == '__main__':
    app.run()
