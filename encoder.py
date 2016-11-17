import cv2
import numpy as np
import wavelets as wl
import video_manager as vm
import reedsolomon as rs

video = cv2.VideoCapture("Lady Gaga - Perfect Illusion-2.mp4")

if video.isOpened():
    key = input()
    
    codec = rs.RSCodec(10)
    
    key_ASCII = []
    key_ASCII.append(ord(character) for character in key)
    
    code = codec.encode(key_ASCII)

    if len(key) > 25:
        print ("Too much characters. Please try one more time.")
        return
    else:
        if len(key) == 0:
            print("No characters was typed. Please try one more time.")
        return
        else:
            vm.encodeVideo(video, code)


