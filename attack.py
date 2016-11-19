import cv2
import numpy as np
import attacks

def RotateVideo(video, angle):
    if (video.isOpened == False):
        video.open()
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output1.avi',fourcc, 24.0, (1920,1080))

    while (video.isOpened()):
        retval, frame = video.read()
        if retval:
            frame = attacks.RotateImg(frame, angle)
            frame = np.uint8(np.round (frame * 255))
            out.write (frame)
        else:
            break
    video.release ()
    out.release ()

def CropVideo(video, percent):
    if (video.isOpened == False):
        video.open()
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output2.avi',fourcc, 24.0, np.uint32((1920,1080)*(1-percent/100)))

    while (video.isOpened()):
        retval, frame = video.read()
        if retval:
            frame = attacks.CropImg(frame, percent)
            frame = np.uint8(np.round (frame * 255))
            out.write (frame)
        else:
            break
    video.release ()
    out.release ()



def ChangeBrightness(video, percent):
    if (video.isOpened == False):
        video.open()
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output1.avi',fourcc, 24.0, (1920,1080))

    while (video.isOpened()):
        retval, frame = video.read()
        if (retval==True):
            frame = attacks.ChangeBrightness(frame, percent)
            frame = np.uint8(np.round (frame * 255))
            out.write (frame)
        else:
            break
    video.release ()
    out.release ()


