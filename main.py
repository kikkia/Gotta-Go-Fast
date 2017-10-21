import numpy as np
import time
from PIL import ImageGrab
import cv2
import pyxinput
from numpy.linalg import lstsq

controllerSet = pyxinput.vController()
controllerRead = pyxinput.rController(1)

def gunIt():
    controllerSet.set_value('TriggerR', 1.0)
    controllerSet.set_value('TriggerL', 0.0)

def slow():
    controllerSet.set_value('TriggerR', 0.2)
    controllerSet.set_value('TriggerL', 0.0)

def hardBrake():
    controllerSet.set_value('TriggerL', 1.0)
    controllerSet.set_value('TriggerR', 0.0)

def lightBrake():
    controllerSet.set_value('TriggerL', 0.3)
    controllerSet.set_value('TriggerR', 0.0)

def straight():
    controllerSet.set_value('AxisLx', 0.0)

def slightRight():
    controllerSet.set_value('AxisLx', 0.1)

def medRight():
    controllerSet.set_value('AxisLx', 0.3)

def hardRight():
    controllerSet.set_value('AxisLx', 0.7)

def crankRight():
    controllerSet.set_value('AxisLx', 1)

def slightLeft():
    controllerSet.set_value('AxisLx', -0.1)

def medLeft():
    controllerSet.set_value('AxisLx', -0.3)

def hardLeft():
    controllerSet.set_value('AxisLx', -0.7)

def crankLeft():
    controllerSet.set_value('AxisLx', -1)


def process_img(originalImage):
    processedImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    processedImage = cv2.Canny(processedImage, threshold1=150, threshold2=250)
    vertices = np.array([[10, 600], [10, 300], [250, 150], [1020, 150], [1270, 300], [1270, 600], [1270, 720], [850, 720], [850, 400],
                         [400, 400], [400, 720], [10, 599]])
    processedImage = roi(processedImage, [vertices])
    processedImage = cv2.GaussianBlur(processedImage, (5,5), 0)
    # Edges needed here TODO: Tweak values, min line length, max line gap
    lines = cv2.HoughLinesP(processedImage, 1, np.pi/180, 180, np.array([]), 100, 5)
    try:
        l1, l2, m1, m2 = drawLines(originalImage, lines)
        cv2.line(originalImage, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(originalImage, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)
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

    return processedImage, originalImage, m1, m2

# Mask off a region of interest since we don't really care about the sky and such
def roi(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(image, mask)


def drawLines(image, lines):
    # if this fails, go with some default line
    try:

        # finds the maximum y value for a lane marker
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []
        for i in lines:
            for ii in i:
                ys += [ii[1], ii[3]]
        min_y = min(ys)
        max_y = 600
        new_lines = []
        line_dict = {}

        for idx, i in enumerate(lines):
            for xyxy in i:
                # These four lines:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0], xyxy[2])
                y_coords = (xyxy[1], xyxy[3])
                A = np.vstack([x_coords, np.ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                if m == 0:
                    x1 = 1280
                    x2 = 1280
                else:
                    x1 = (min_y - b) / m
                    x2 = (max_y - b) / m

                line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_lanes = {}

        for idx in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]

            else:
                found_copy = False

                for other_ms in final_lanes_copy:

                    if not found_copy:
                        if abs(other_ms * 1.2) > abs(m) > abs(other_ms * 0.8):
                            if abs(final_lanes_copy[other_ms][0][1] * 1.2) > abs(b) > abs(
                                            final_lanes_copy[other_ms][0][1] * 0.8):
                                final_lanes[other_ms].append([m, b, line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [[m, b, line]]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(np.mean(x1s)), int(np.mean(y1s)), int(np.mean(x2s)), int(np.mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        print(str(e))


lastTime = time.time()
while True:
    screen = np.array(ImageGrab.grab(bbox=(0,40, 1280, 720)))
    processedScreen, original, m1, m2 = process_img(screen)
    print("Rendering {} fps".format(1 / (time.time() - lastTime)))
    lastTime = time.time()
    cv2.imshow('window', processedScreen)
    cv2.imshow('window', original)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    if m1 < 0 and m2 < 0:
        print("here right \n")
        medRight()
    elif m1 > 0 and m2 > 0:
        print("here left \n")
        medLeft()
    else:
        straight()

    slow()


