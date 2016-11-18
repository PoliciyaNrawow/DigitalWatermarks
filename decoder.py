import cv2
import numpy as np
import wavelets as wl
import video_manager as vm
import useful_tools as ut
import reedsolomon as rs

orgVideo = cv2.VideoCapture("Lady-Gaga-Test.mp4")
encVideo = cv2.VideoCapture("output.avi")

key  = input()

codec = rs.RSCodec(10)

key_ASCII = []
for character in key:
    key_ASCII.append(ord(character))
    
code = codec.encode(key_ASCII)

words = vm.decodeVideo(orgVideo, encVideo, code)

print (words)
