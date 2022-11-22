import numberFinder
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'D:\\Softwares\\Tesseract\\tesseract.exe'

###############################################################

roiPnts = [[(1218, 70), (1540, 126), 'number', 'date'],
               [(1200, 332), (1540, 416), 'number', 'amt'],
               [(212, 448), (520, 498), 'number', 'accNo'],
               [(4, 760), (1590, 888), 'micr', 'micr'],
               [(116, 170), (1240, 250), 'text', 'name']]


###############################################################


def stack_images(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def crop(img, fname):
    data = {'name': fname}
    img = cv2.resize(img, (1600, 900))
    cv2.imwrite('fileUpload/procFile/' + fname, img)

    imgShow = img.copy()
    imgMask = np.zeros_like(imgShow)

    for x, r in enumerate(roiPnts):
        cv2.rectangle(imgMask, ((r[0][0]), r[0][1]), ((r[1][0]), r[1][1]), (0, 255, 0), cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)
        imgCrop = img[r[0][1]:r[1][1], r[0][0]:r[1][0]]

        if r[2] == 'number':
            if r[3] == 'date':
                num = numberFinder.predict_number(imgCrop, r[3])
                data[r[3]] = num

            elif r[3] == 'accNo':
                gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
                th, threshed = cv2.threshold(gray, 150, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
                morphed = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, np.ones((2, 2)))
                num = pytesseract.image_to_string(morphed)
                num.strip()
                num = ''.join(num.splitlines())
                data[r[3]] = num
            else:
                num = numberFinder.predict_number(imgCrop, r[3])
                data[r[3]] = num

        elif r[2] == 'text':
            text = pytesseract.image_to_string(imgCrop)
            text.strip()
            text = ''.join(text.splitlines())
            data[r[3]] = text
    return data
