from flask import Flask, render_template, request
import numpy as np
from werkzeug.utils import secure_filename
import os
import cv2
import tensorflow
from keras.models import load_model

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "upload"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files['digit']
    validExt = ['png', 'jpg', 'jpeg', 'tif', 'eps', 'gif']
    extension = f.filename.split('.')[1]
    if extension not in validExt:
        return "Not a valid extension"

    fname = secure_filename(str(len(os.listdir('upload')))) + "." + extension
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
    img = cv2.imread("upload\\" + fname)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binarizing and removing noise from the image
    th, threshed = cv2.threshold(gray, 160, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, np.ones((2, 2)))
    resized = cv2.resize(morphed, (28, 28), interpolation=cv2.INTER_AREA)
    newImg = tensorflow.keras.utils.normalize(resized, axis=1)
    newImg = np.array(newImg).reshape(-1, 28, 28, 1)

    # Loading the model
    model = load_model("model/number.h5")

    # Predicting the output
    prediction = model.predict(newImg)

    # returning the result
    op = np.argmax(prediction)
    return render_template("result.html", res=op)


if __name__ == "__main__":
    app.run()
