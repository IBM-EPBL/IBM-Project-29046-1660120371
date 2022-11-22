import cv2
import numpy as np
from tensorflow import keras
import tensorflow as tf

model = keras.models.load_model('models/number.h5')


# Function to sort the contours
def sort_contours(cnts, method="left-to-right"):
    # Initialize the reverse flag and sort index
    reverse = False
    i = 0

    # Handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # Handle if we are sorting against the y-coordinate rather than the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # Construct the list of bounding boxes and sort them from top to bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))

    # Return the list of sorted contours and bounding boxes
    return cnts


# Function to predict the numbers in the image
def predict_number(imgO, name):
    res = ""

    # Converting the image to grayscale
    gray = cv2.cvtColor(imgO, cv2.COLOR_BGR2GRAY)

    # Binarizing and removing noise from the image
    th, threshed = cv2.threshold(gray, 160, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, np.ones((2, 2)))

    # Finding all possible contours in the image and sorting them according to their order of occurances from left to right
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sort_contours(cnts)

    # Working with each of the contours
    for cnt in cnts:

        # Storing the values of bounding box of the current contour
        x, y, w, h = cv2.boundingRect(cnt)

        # Setting the minimum area a contour must satisfy and starting next iteration if condition is not met
        minArea = 100
        if (h * w < minArea) or (w > h):
            continue

        try:
            # Cropping the image with the bounding box info
            cropped = threshed[y - 5:y + h + 5, x - 5:w + x + 5]
            # Preprocessing the cropped image as per our model need
            resized = cv2.resize(cropped, (28, 28), interpolation=cv2.INTER_AREA)
        except:
            # Cropping the image with the bounding box info
            cropped = threshed[y:y + h, x:w + x]
            # Preprocessing the cropped image as per our model need
            resized = cv2.resize(cropped, (28, 28), interpolation=cv2.INTER_AREA)

        # Drawing contours for visual purpose
        cv2.rectangle(imgO, (x, y), (x + w, y + h), (255, 0, 255), 1, cv2.LINE_AA)

        newImg = tf.keras.utils.normalize(resized, axis=1)
        newImg = np.array(newImg).reshape(-1, 28, 28, 1)

        # Predicting the output
        prediction = model.predict(newImg)

        # Storing the result
        op = np.argmax(prediction)
        res += str(op)

    return res
