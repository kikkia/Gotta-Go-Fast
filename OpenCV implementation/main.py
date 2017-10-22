import numpy as np

import time
from PIL import ImageGrab
import cv2
import queue

from drawTrack import drawTrack
from inputs import gunIt, straight, medLeft, medRight, slow, lightBrake, hardRight, hardLeft, slightRight, slightLeft


def process_img(originalImage):
    #defaults
    m1 = 0
    m2 = 0
    l1 = (0, 1, 2, 3)
    l2 = (0, 1, 2, 3)

    processedImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    processedImage = cv2.Canny(processedImage, threshold1=150, threshold2=250)
    vertices = np.array([[10, 600], [10, 450], [250, 300], [1020, 300], [1270, 450], [1270, 600], [1270, 720], [600, 400], [10, 720]])
    processedImage = roi(processedImage, [vertices])
    processedImage = cv2.GaussianBlur(processedImage, (5,5), 0)
    # Edges needed here TODO: Tweak values, min line length, max line gap
    lines = cv2.HoughLinesP(processedImage, 1, np.pi/180, 180, np.array([]), 100, 5)
    try:
        l1, l2, m1, m2 = drawTrack(originalImage, lines)
        cv2.line(originalImage, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 5)
        cv2.line(originalImage, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 5)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processedImage, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
            except:
                pass
    except:
        pass

    return processedImage, originalImage, m1, m2, l1, l2

def intersection(line1, line2):
    xdiff = (line1[0] - line1[2], line2[0] - line2[2])
    ydiff = (line1[1] - line1[3], line2[1] - line2[3])  # Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        # If parallel lines go straight
        return 640, 360

    d = (det([line1[0], line1[1]], [line1[2], line1[3]]), det([line2[0], line2[1]], [line2[2], line2[3]]))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# Mask off a region of interest since we don't really care about the sky and such
def roi(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(image, mask)

lastTime = time.time()
queue = queue.Queue(maxsize=6)
while True:
    screen = np.array(ImageGrab.grab(bbox=(0,40, 1280, 720)))
    processedScreen, original, m1, m2, l1, l2 = process_img(screen)
    print("Rendering {} fps".format(1 / (time.time() - lastTime)))
    lastTime = time.time()

    inter = intersection(l1, l2)
    inter = (min(1280, inter[0]), inter[1])
    inter = (max(0, inter[0]), inter[1])
    if queue.full():
        queue.get()
    queue.put(inter[0])
    meanX = np.math.floor(np.mean(queue.queue))
    meanX = min(1280, meanX)
    meanX = max(0, meanX)
    print(meanX)

    cv2.circle(original, (int(meanX), 360), 10, (255, 0, 0), thickness= 4)

    cv2.imshow('window', original)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    inter = intersection(l1, l2)
    if queue.full():
        queue.get()
    queue.put(inter[0])
    meanX = np.mean(queue.queue)
    print(meanX)
    if 1050 > meanX > 800:
        medRight()
        lightBrake()
    elif 250 < meanX < 500:
        medLeft()
        lightBrake()
    elif meanX < 250:
        hardLeft()
        lightBrake()
    elif meanX > 1050:
        hardRight()
        lightBrake()
    elif 650 < meanX < 800:
        slightRight()
    elif 500 < meanX < 630:
        slightLeft()
    else:
        straight()

    if m1 < 0 and m2 < 0:
        medRight()
        lightBrake()
    elif m1 > 0 and m2 > 0:
        medLeft()
        lightBrake()


    slow()


