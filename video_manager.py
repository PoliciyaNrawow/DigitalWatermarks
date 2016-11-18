import cv2
import numpy as np
import wavelets as wl
import scipy as sp
import reedsolomon as rs


def encodeVideo(video, key):
    
    if video.isOpened() == False:
        video.open()
    
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter('output.avi',fourcc, 25.0, (1920, 1080))

    iteration = 0

    while (video.isOpened()):
        retval, frame = video.read()
        if retval == True:
            transformedFrame = wl.TransformImage(frame, ((key[iteration % 25] >> iteration % 8) & 1))
            transformedFrame = np.uint8(transformedFrame * 255)
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
    
    watermarkArray = []

    iteration = 0

    codec = rs.RSCodec(10)
    
    while (originalVideo.isOpened() & encodedVideo.isOpened()):
        orgRetVal, orgFrame = originalVideo.read()
        encRetVal, encFrame = encodedVideo.read()
        
        words = []
        
        if orgRetVal == True & encRetVal == True:
            watermarkArray = np.append(watermarkArray, wl.RetrieveWat(encFrame, orgFrame, key[iteration % 25]))
            iteration += 1
            print(iteration)
            if len(watermarkArray) == 25:
                print("we are here")
                watermarkArray = np.array(watermarkArray)
                watermarkArray.astype(np.uint8)
                try:
                    word_ASCII = codec.decode(watermarkArray)
                except rs.ReedSolomonError:
                    print("Too much errors")
                else:
                    print("lol")
                    word = [chr(i) for i in word_ASCII]
                    print(word)
                    words.append(word)
                finally:
                    watermarkArray = []
        else:
            return words

