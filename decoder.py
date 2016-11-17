import cv2
import numpy as np
import wavelets as wl
import video_manager as vm
import useful_tools as ut

orgVideo = cv2.VideoCapture("Lady Gaga - Perfect Illusion-2.mp4")
encVideo = cv2.VideoCapture("output.mp4")

key  = input()

codec = rs.RSCodec(10)

key_ASCII = []
key_ASCII.append(ord(character) for character in key)
    
code = codec.encode(key_ASCII)

words = vm.decodeVideo(orgVideo, encVideo, code)

print (ut.most_common(words))
