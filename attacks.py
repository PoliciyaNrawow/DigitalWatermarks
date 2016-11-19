import cv2
import numpy as np
import pywt
import scipy.linalg as linalg

def RotateImg (img, ang):
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32(img) * 1.0 / 255
    if hasattr(img, 'shape'):
        image_center = tuple(np.array(img.shape)/2)
        shape = tuple(img.shape)
    else :
        image_center = tuple(np.array((img.width/2, img.height/2)))
        shape = (img.width, img.height)
    #print(shape)
    rot_mat = cv2.getRotationMatrix2D((image_center[0],image_center[1]), ang, 1)
    #image = np.asarray( image[:,:]
    rotated_image = cv2.warpAffine(img, rot_mat, (shape[1],shape[0]), flags=cv2.INTER_LINEAR)
    return rotated_image
    
def ChangeBrightness (img, percent):
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32(img) * 1.0 / 255
    img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    img1[:,:,0] *= percent / 100
    img = cv2.cvtColor (img1, cv2.COLOR_YCrCb2BGR)
    return img

def CropImg (img, percent):
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32(img) * 1.0 / 255
    if hasattr(img, 'shape'):
        shape = tuple(img.shape)
    else:
        shape = (img.width, img.height)
    percent /= 100
    cropped = img[np.uint32(shape[0] * percent / 2):np.uint32((shape[0]*(1-percent * 2))), np.uint32(shape[1] * percent / 2):np.uint32((shape[1]*(1-percent * 2))),:]
    #print (cropped)
    return cropped
    
def NormalizeImg (img, orig):
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32(img) * 1.0 / 255

    norm = np.linalg.norm(img)
    orig_norm = np.linalg.norm(orig)
    img *= orig_norm / norm
    return img

    
