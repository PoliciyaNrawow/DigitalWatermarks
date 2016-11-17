import cv2
import numpy as np
import wavelets as wl
import scipy as sp
import reedsolomon as rs


def encodeVideo(video, key):
    
    if video.isOpened() == False:
        video.open()
    
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter('output.mp4',fourcc, 25.0, (1920, 1080))

    iteration = 0

    while (video.isOpened()):
        retval, frame = video.read()
        if retval == True:
            transformedFrame = wl.TransformImage(frame, key[iteration % 25])
            iteration += 1
            out.write(transformedFrame)
        else:
            break

    video.release()
    out.release()

def decodeVideo(originalVideo, encodedVideo, key):
    if originalVideo.isOpened() == False:
        originalVideo.open()
    
    if encodedVideo.isOpened() == False:
        encodedVideo.open()
    
    watermarkArray = []

    iteration = 0
    
    while (originalVideo.isOpened() && encodedVideo.isOpened()):
        orgRetVal, orgFrame = originalVideo.read()
        encRetVal, encFrame = encodedVideo.read()
        
        if orgRetVal == True && encRetVal == True:
            watermarkArray.append(wl.RetrieveWat(encFrame, orgFrame, key[iteration % 25]))
            iteration += 1
            if len(watermarkArray) == 25 :
                watermarkArray.astype(numpy.uint8)
                try:
                    word_ASCII = rs.decode(watermarkArray)
                except ReedSolomonError:
                    print("Too much mistakes")
                else:
                    word = [chr(i) for i in word_ASCII]
                    print(word)
                    words.append(word)
        else:
            return words

