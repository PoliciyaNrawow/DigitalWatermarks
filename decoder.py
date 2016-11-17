import cv2
import numpy as np
import wavelets as wl
import video_manager as vm
import useful_tools as ut

orgVideo = cv2.VideoCapture()
encVideo = cv2.VideoCapture()

words = vm.decodeVideo(orgVideo, encVideo)

print (ut.most_common(words))
