import cv2
import numpy as np
import wavelets as wl
import scipy as sp
import reedsolomon as rs
import attacks


def encodeVideo(video, key):
    
    if video.isOpened() == False:
        video.open()
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.avi',fourcc, 24.0, (1920,1080))

    iteration = 0

    while (video.isOpened()):
        retval, frame = video.read()
        if retval == True:
            #if (iteration % 22 < 11):
            #    transformedFrame = wl.TransformImage(frame, 0)
            #else:
            transformedFrame = wl.TransformImage(frame, ((key[(iteration // 8) % 11] >> (iteration % 8)) & 1))
            transformedFrame = np.uint8(np.round(transformedFrame * 255))
            iteration += 1
            print(iteration)
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
    
    watermarkArray = np.uint8 (np.zeros (11))

    iteration = 0
    preambuleReceived = True
    preambuleCntr = 0
    watIter = 0
    codec = rs.RSCodec(8)
    words = []
    while (originalVideo.isOpened() & encodedVideo.isOpened()):
        orgRetVal, orgFrame = originalVideo.read()
        encRetVal, encFrame = encodedVideo.read()
        
                
        if orgRetVal == True & encRetVal == True:
            if (preambuleReceived):
                tmp = wl.RetrieveWat(attacks.RotateImg (encFrame, 1), orgFrame, (key[watIter // 8] >> (watIter % 8)) & 1)
                watermarkArray[watIter // 8] |= (tmp << (watIter % 8))
                watIter += 1
            elif (wl.RetrieveWat(encFrame, orgFrame, 0) == 0):
                preambuleCntr += 1
            else:
                preambuleCntr = 0
            if (preambuleCntr == 11):
                preambuleReceived = True
            iteration += 1
            #print(iteration)
            if (watIter == 88):
                print("we are here")
                watermarkArray = np.array(watermarkArray)
                #watermarkArray.astype(np.uint8)
                try:
                    word_ASCII = codec.decode(watermarkArray)
                except rs.ReedSolomonError:
                    print("Too much errors")
                else:
                    print("lol")
                #word = [chr(i) for i in watermarkArray]
                    word = [chr(i) for i in word_ASCII]
                    print(word)
                    words.append(word)
                finally:
                    preambuleCntr = 0
                    watIter = 0
                    watermarkArray = np.uint8 (np.zeros(11))
                    #preambuleReceived = False
        else:
            return words

