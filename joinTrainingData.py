import os
import numpy as np

filename = "combinedTrainingData.npy"

if os.path.isfile("training_data.npy"):
    trainingData = list(np.load("training_data.npy"))
print(len(trainingData))
fileCount = 1
while True:
    try:
        for data in list(np.load("training_data" + str(fileCount) + ".npy")):
            trainingData.append([data[0], data[1]])
        print(len(trainingData))
        fileCount += 1
    except Exception as e:
        print(str(e))
        break

print(len(trainingData))
np.save(filename, trainingData)
print("saved")
