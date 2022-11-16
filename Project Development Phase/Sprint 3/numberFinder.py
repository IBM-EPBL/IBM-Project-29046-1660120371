import cv2
import numpy as np
import helperFunctions
from tensorflow import keras
import tensorflow as tf

model = keras.models.load_model('models/number.h5')
path = "fileUpload/test/"


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

    # Converting the image to Grayscale
    gray = cv2.cvtColor(imgO, cv2.COLOR_BGR2GRAY)

    # Binarizing and removing noise from the image
    th, threshed = cv2.threshold(gray, 150, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, np.ones((2, 2)))


    # Finding all possible contours in the image and sorting them according to their order of occurances from left to right
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sort_contours(cnts)

    # Working with each of the contours
    for cnt in cnts:

        # Storing the values of bounding box of the current contour
        x, y, w, h = bbox = cv2.boundingRect(cnt)
        # Setting the minimum area a contour must satisfy and starting next iteration if condition is not met
        minArea = 180
        if (h * w < minArea) or (w > h) :
            continue

        try:
            # Cropping the image with the bounding box info
            cropped = morphed[y - 5:y + h + 5, x - 5:w + x + 5]
            # Preprocessing the cropped image as per our model need
            resized = cv2.resize(cropped, (28, 28), interpolation=cv2.INTER_AREA)
        except:
            # Cropping the image with the bounding box info
            cropped = morphed[y:y + h, x:w + x]
            # Preprocessing the cropped image as per our model need
            resized = cv2.resize(cropped, (28, 28), interpolation=cv2.INTER_AREA)


        # Drawing contours for visual purpose
        cv2.rectangle(imgO, (x, y), (x + w, y + h), (255, 0, 255), 1, cv2.LINE_AA)

        # print(resized.shape)
        newImg = tf.keras.utils.normalize(resized, axis=1)
        newImg = np.array(newImg).reshape(-1, 28, 28, 1)

        # Predicting the output
        prediction = model.predict(newImg)

        # Storing the result
        op = np.argmax(prediction)
        res += str(op)

    cv2.imshow(name, imgO)
    cv2.waitKey(0)
    return res


# Function to predict the dates
def predict_date(image, name):
    res = ''

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(image, 120, 890)
    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(edged, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 191, 5)
    cv2.imshow("adaptive thres", thresh)
    thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
    # thresh = cv2.dilate(thresh, None, iterations=50)
    # thresh = cv2.erode(thresh, None, iterations=50)

    # Find the contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # For each contour, find the bounding rectangle and draw it
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # cv2.imshow('img', image)
    # imgContour = imgO.copy()
    # imgThres = helperFunctions.pre_processing(imgO)
    # biggest = helperFunctions.get_contours(imgThres, imgContour)
    # if biggest.size != 0:
    #     pass
    # else:
    #     return 'No Cheque Detected'
