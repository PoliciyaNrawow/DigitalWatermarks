import cv2
import numpy as np
import wavelets as wl
import video_manager as vm
import useful_tools as ut
import reedsolomon as rs
import attack

orgVideo = cv2.VideoCapture("Lady-Gaga-Test.mp4")
encVideo = cv2.VideoCapture("output.avi")
attack.ChangeBrightness (encVideo, 95)
#attack.RotateVideo (encVideo, 1)
encVideo = cv2.VideoCapture("output1.avi")
#attack.CropVideo (encVideo, 3)
#encVideo = cv2.VideoCapture("outputi2.avi")
print ("Enter key:")
key  = input()

codec = rs.RSCodec(8)

key_ASCII = []
for character in key:
    key_ASCII.append(ord(character))
    
code = codec.encode(key_ASCII)

words = vm.decodeVideo(orgVideo, encVideo, code)

print (words)
