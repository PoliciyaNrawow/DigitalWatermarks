import cv2
import numpy as np
import wavelets as wl
#import scipy as sp


def encodeVideo(video):
    
    if video.isOpened() == False:
        video.open()
    
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter('output.mpeg',fourcc, 25.0, (1280, 720))

    while (video.isOpened()):
        retval, frame = video.read()
        if retval == True:
            transformedFrame = wl.TransformImage(frame)
            out.write(transformedFrame)
        else:
            break

    video.release()
    out.release()

def decodeVideo(originalVideo, encodedVideo):
    if originalVideo.isOpened() == False:
        originalVideo.open()
    
    if encodedVideo.isOpened() == False:
        encodedVideo.open()
    
    watermarkArray = []
    
    while (originalVideo.isOpened() && encodedVideo.isOpened()):
        orgRetVal, orgFrame = originalVideo.read()
        encRetVal, encFrame = encodedVideo.read()
        
        if orgRetVal == True && encRetVal == True:
            watermarkArray.append(wl.RetrieveWat(encFrame, orgFrame))
            if len(watermarkArray) == 25 :
                res = np.array(watermarkArray[0])
                for i in range(1, 24):
                    res += np.array(watermarkArray[i])
                res = res/25
                res.astype(numpy.uint8)
                
