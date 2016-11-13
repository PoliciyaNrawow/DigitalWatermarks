import cv2
import numpy as np
import wavelets as wl
import video_manager as vm

orgVideo = cv2.VideoCapture()
encVideo = cv2.VideoCapture()

words = vm.decodeVideo(orgVideo, encVideo)
