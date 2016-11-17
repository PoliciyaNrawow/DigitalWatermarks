import cv2
import numpy as np
import pywt
import scipy.linalg as linalg

def RotateImg (image, ang):
    if hasattr(image, 'shape'):
        image_center = tuple(np.array(image.shape)/2)
        shape = tuple(image.shape)
    else :
        image_center = tuple(np.array((image.width/2, image.height/2)))
        shape = (image.width, image.height)
    print(shape)
    rot_mat = cv2.getRotationMatrix2D((image_center[0],image_center[1]), ang, 1)
    #image = np.asarray( image[:,:]
    rotated_image = cv2.warpAffine(image, rot_mat, (shape[1],shape[0]), flags=cv2.INTER_LINEAR)
    return rotated_image
    
def ChangeBrightness (img, percent):
    img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    img1[:,:,0] *= percent / 100
    img = cv2.cvtColor (img1, cv2.COLOR_YCrCb2BGR)
    return img

def CropImg (image, percent):
    if hasattr(image, 'shape'):
        shape = tuple(image.shape)
    else:
        shape = (image.width, image.height)
    percent /= 100
    cropped = image[np.uint32(shape[0] * percent / 2):np.uint32((shape[0]*(1-percent * 2))), np.uint32(shape[1] * percent / 2):np.uint32((shape[1]*(1-percent * 2))),:]
    print (cropped)
    return cropped
    
def NormalizeImg (img, orig):
    norm = np.linalg.norm(img)
    orig_norm = np.linalg.norm(orig)
    img *= orig_norm / norm
    return img

    
