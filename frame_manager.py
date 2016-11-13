import cv2
import numpy as np
#import scipy as sp

cap = cv2.VideoCapture("buy.mov")

#if video.isOpened() == False:
#    video.open()

retval = True

while (retval):
    retval, frame = cap.read()
    if retval == True:
    #cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
