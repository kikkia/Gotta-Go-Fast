from pymouse import PyMouse
from pykeyboard import PyKeyboard
import cv2
import numpy

mouse = PyMouse()
k = PyKeyboard()

def SingleSelect(x, y):
    mouse.click(x, y)

def MultiSelect(startX, startY, endX, endY):
    mouse.move(startX,startY)
    mouse.drag(endX, endY)

def SimilarSelect(x, y):
    mouse.click(x, y, 1, 2)

def Move(x,y):
    k.tap_key('m')
    mouse.click(x, y)

def Attack(x, y):
    k.tap_key('a')
    mouse.click(x, y)

def BuildPower(x,y):
    k.press_keys([k.alt_key, ','])
    k.tap_key('b')
    k.tap_key('p')
    k.press_keys(k.shift_key)
    mouse.click(x,y)
    k.release_key(k.shift_key)
    k.tap_key(k.escape_key)

def ReadNumber(upperLeft, lowerRight):
    processedImage = cv2.imread('C:/Users/quade/workspace/Gotta-Go-Fast/NumberReadTest4.jpg')
    processedImage = cv2.cvtColor(processedImage, cv2.COLOR_BGR2GRAY)
    processedImage = cv2.threshold(processedImage, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(processedImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0]
    digitCnts = []

    # loop over the digit area candidates
    i = 0
    j=0
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)

        i+= 1
        # if the contour is sufficiently large, it must be a digit
        if w >= 1 and (h >= 1 and h <= 100):
            digitCnts.append(c)
            j+= 1
            print(x, '/', y, ':', w, h)
    print(i)
    print(j)
    ctr = numpy.array(digitCnts).reshape((-1, 1, 2)).astype(numpy.int32)
    blank = cv2.imread("C:/Users/quade/workspace/Gotta-Go-Fast/blank.jpg")
    cv2.drawContours(blank, [ctr], -1, (0, 255, 0), 3)
    cv2.imshow('window', processedImage)
    cv2.imshow('blankwindow', blank)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # loop over the digit area candidates

ReadNumber(1,1)