import cv2
import numpy as np
import time
from PIL import ImageGrab

def initRead():
    global model
    samples = np.loadtxt('generalsamples.data', np.float32)
    responses = np.loadtxt('generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))
    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)

def ReadValue(startX, startY, endX, endY):
    im = np.array(ImageGrab.grab(bbox=(startX, startY, endX, endY)))

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    thresh = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    ans = ''

    for cnt in contours:
        if cv2.contourArea(cnt) > 10:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 10:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                string = str(int((results[0][0])))
                if (string == '0' or string == '1' or string == '7'):
                    if (np.average(dists) < 1200000):
                        ans += string
                elif (string == '3' or string == '5'):
                    if (np.average(dists) < 1600000):
                        ans += string
                elif (np.average(dists) < 1400000):
                    ans += string
    return ans[::-1]

#######   training part    ###############
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.ml.KNearest_create()
#model.train(samples,responses)
model.train(samples, cv2.ml.ROW_SAMPLE, responses)
############################# testing part  #########################

start_time = time.time()
im = cv2.imread('C:/Users/quade/workspace/Gotta-Go-Fast/NumberReadTest3.jpg')

out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
thresh = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
ans = ''

for cnt in contours:
    if cv2.contourArea(cnt)>10:
        [x,y,w,h] = cv2.boundingRect(cnt)
        if  h>10:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            roismall = roismall.reshape((1,100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
            string = str(int((results[0][0])))
            if(string == '0' or string == '1' or string == '7'):
                if(np.average(dists) < 1200000):
                    cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))
                    ans+=string
            elif (string == '3' or string == '5'):
                if (np.average(dists) < 1600000):
                    cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))
                    ans += string
            elif(np.average(dists) < 1400000):
                cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
                ans += string

print("--- %s seconds ---" % (time.time() - start_time))
print(ans[::-1])
cv2.imshow('im',im)
cv2.imshow('out',out)
cv2.waitKey(0)