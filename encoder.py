import cv2
import numpy as np
import wavelets as wl
import video_manager as vm

video = cv2.VideoCapture()

if video.isOpened():
    key = input()
    if len(key) > 25:
        print ("Too much characters. Please try one more time.")
        return
    else:
        if len(key) == 0:
            print("No characters was typed. Please try one more time.")
        else:
            vm.encodeVideo(video, key)


