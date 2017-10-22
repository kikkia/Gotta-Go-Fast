import numpy as np
import os
import time
import cv2

from getControllerData import getDrivingState, sample_first_joystick, XInputJoystick
from getDisplay import getDisplay

def formatDrivingState(dState):
    for i in range(0, 4):
        if -0.12 < dState[i] < .12:
            dState[i] = 0
    return dState

def controllerToOutput(state):
    # [0: Low breaks, 1: med brakes, 2: full brakes, 3: low gas, 4: med gas, 5: full gas,
    #  6: slight X stick+, 7: med X stick+, 8: full X stick+, 9: slight X Stick -, 10: med Xstick -, 11: full xstick-,
    #  12: low gas and slight X+, 13: low gas and med X+, 14: low gas and full X+,
    #  15: low gas and slight X-, 16: low gas and med X+, 17: low gas and full X-,
    #  18: med gas and slight X+, 19: med gas and med X+, 20: med gas and full X+, 
    #  21: med gas and slight X-, 22: med gas and med X-, 23: med gas and full X-,
    #  24: full gas and slight X+, 25: full gas and med X+, 26: full gas and full X+, 
    #  27: full gas and slight X-, 28: full gas and med X-, 29: full gas and full X-,
    #  30: low brake and slight X+, 31: low brake and med X+, 32: low brake and full X+,
    #  33: low brake and slight X-, 34: low brake and med X+, 35: low brake and full X-,
    #  36: med brake and slight X+, 37: med brake and med X+, 38: med brake and full X+,
    #  39: med brake and slight X-, 40: med brake and med X-, 41: med brake and full X-,
    #  42: full brake and slight X+, 43: full brake and med X+, 44: full brake and full X+,
    #  45: full brake and slight X-, 46: full brake and med X-, 47: full brake and full X-,
    #  48: coast]
    output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
    if .3 > state[1] > 0 and .2 >= state[2] > 0:
        output[12] = 1
    elif .3 > state[1] > 0 and .4 > state[2] > .2:
        output[13] = 1
    elif .3 > state[1] > 0 and state[2] >= .4:
        output[14] = 1
    elif .3 > state[1] > 0 and -.2 <= state[3] < 0:
        output[15] = 1
    elif .3 > state[1] > 0 and -.4 < state[3] < -.2:
        output[16] = 1
    elif .3 > state[1] > 0 and state[3] <= -.4:
        output[17] = 1
    elif .7 > state[1] >= .3 and .2 >= state[2] > 0:
        output[18] = 1
    elif .7 > state[1] >= .3 and .4 > state[2] > .2:
        output[19] = 1
    elif .7 > state[1] >= .3 and state[2] >= .4:
        output[20] = 1
    elif .7 > state[1] >= .3 and -.2 <= state[3] < 0:
        output[21] = 1
    elif .7 > state[1] >= .3 and -.4 < state[3] < -.2:
        output[22] = 1
    elif .7 > state[1] >= .3 and state[3] <= -.4:
        output[23] = 1
    elif state[1] >= .7 and .2 >= state[2] > 0:
        output[24] = 1
    elif state[1] >= .7 and .4 > state[2] > .2:
        output[25] = 1
    elif state[1] >= .7 and state[2] >= .4:
        output[26] = 1
    elif state[1] >= .7 and -.2 <= state[3] < 0:
        output[27] = 1
    elif state[1] >= .7 and -.4 < state[3] < -.2:
        output[28] = 1
    elif state[1] >= .7 and state[3] <= -.4:
        output[29] = 1
    elif .3 > state[0] > 0 and .2 >= state[2] > 0:
        output[30] = 1
    elif .3 > state[0] > 0 and .4 > state[2] > .2:
        output[31] = 1
    elif .3 > state[0] > 0 and state[2] >= .4:
        output[32] = 1
    elif .3 > state[0] > 0 and -.2 <= state[3] < 0:
        output[33] = 1
    elif .3 > state[0] > 0 and -.4 < state[3] < -.2:
        output[34] = 1
    elif .3 > state[0] > 0 and state[3] <= -.4:
        output[35] = 1
    elif .7 > state[0] >= .3 and .2 >= state[2] > 0:
        output[36] = 1
    elif .7 > state[0] >= .3 and .4 > state[2] > .2:
        output[37] = 1
    elif .7 > state[0] >= .3 and state[2] >= .4:
        output[38] = 1
    elif .7 > state[0] >= .3 and -.2 <= state[3] < 0:
        output[39] = 1
    elif .7 > state[0] >= .3 and -.4 < state[3] < -.2:
        output[40] = 1
    elif .7 > state[0] >= .3 and state[3] <= -.4:
        output[41] = 1
    elif state[0] >= .7 and .2 >= state[2] > 0:
        output[42] = 1
    elif state[0] >= .7 and .4 > state[2] > .2:
        output[43] = 1
    elif state[0] >= .7 and state[2] >= .4:
        output[44] = 1
    elif state[0] >= .7 and -.2 <= state[3] < 0:
        output[45] = 1
    elif state[0] >= .7 and -.4 < state[3] < -.2:
        output[46] = 1
    elif state[0] >= .7 and state[3] <= -.4:
        output[47] = 1
    elif state[1] >= .7:
        output[5] = 1
    elif .7 > state[1] >= .3:
        output[4] = 1
    elif .3 > state[1] > 0:
        output[3] = 1
    elif state[0] >= .7:
        output[2] = 1
    elif .7 > state[0] >= .3:
        output[1] = 1
    elif .3 > state[0] > 0:
        output[0] = 1
    elif .2 >= state[2] > 0:
        output[6] = 1
    elif .4 > state[2] > .2:
        output[7] = 1
    elif state[2] >= .4:
        output[8] = 1
    elif -.2 <= state[3] < 0:
        output[9] = 1
    elif -.4 < state[3] < -.2:
        output[10] = 1
    elif state[3] <= -.4:
        output[11] = 1
    else:
        output[48] = 1
    return output

trainingFilename = "training_data"

if os.path.isfile(trainingFilename + ".npy"):
    print("File exsists, loading prev data")
    trainingData = list(np.load(trainingFilename + ".npy"))
else:
    print("no previous data, making data file")
    trainingData = []

lastTime = time.time()
drivingState = [0, 0, 0, 0, ]
joysticks = XInputJoystick.enumerate_devices()
j = joysticks[0]
dry_run = 0
file_counter = 0

if not dry_run:
    for i in range(0, 5):
        print(i + 1)
        time.sleep(1)

while True:
    screen = np.array(getDisplay(region=(0, 40, 1280, 760)))
    j.dispatch_events()
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (160, 90))
    drivingState = formatDrivingState(drivingState)
    output = controllerToOutput(drivingState)
    trainingData.append([screen, output])

    if dry_run:
        print(output)

    if len(trainingData) %500 == 0 and not dry_run:
        print(len(trainingData))
        print("Rendering {} fps".format(500 / (time.time() - lastTime)))
        lastTime = time.time()
        np.save(trainingFilename + ".npy", trainingData)

    if len(trainingData) %5000 == 0 and not dry_run:
        file_counter += 1
        print(len(trainingData))
        print("Saving to new file, total {}".format(file_counter * 5000))
        print("Rendering {} fps".format(500 / (time.time() - lastTime)))
        lastTime = time.time()
        np.save(trainingFilename + str(file_counter) + ".npy", trainingData)
        trainingData = []

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


    @j.event
    def on_axis(axis, value):
        left_speed = 0
        right_speed = 0

        # print('axis', axis, value)
        if axis == "left_trigger":
            left_speed = value
            drivingState[0] = value
        elif axis == "right_trigger":
            right_speed = value
            drivingState[1] = value
        elif axis == "l_thumb_x":
            if value > 0:
                drivingState[2] = value
                drivingState[3] = 0
            else:
                drivingState[3] = value
                drivingState[2] = 0
        j.set_vibration(left_speed, right_speed)