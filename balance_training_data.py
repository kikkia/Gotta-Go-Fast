import numpy as np
import pandas
from collections import Counter
from random import shuffle
import cv2

train_data = np.load('combinedTrainingData.npy')



for data in train_data:
    img = data[0]
    choice = data[1]


# dataF = pandas.DataFrame(train_data)
# print(dataF.head())
# print(Counter(dataF[1].apply(str)))

# for data in train_data:
#     image = data[0]
#     controls = data[1]
#     cv2.imshow('test', image)
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break

