import cv2
import numpy as np
import wavelets as wl
import video_manager as vm
import reedsolomon as rs
import sys

video = cv2.VideoCapture("Lady-Gaga-Test.mp4")

if video.isOpened():
    key = input()
    
    codec = rs.RSCodec(5)
    
    key_ASCII = []
    
    for character in key:
        print(ord(character))
        key_ASCII.append(ord(character))
    
    code = codec.encode(key_ASCII)

    if len(key) > 5:
        sys.exit("Too much characters. Please try one more time.")
    elif len(key) == 0:
        sys.exit("No characters was typed. Please try one more time.")
    else:
            vm.encodeVideo(video, code)


