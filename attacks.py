import cv2
import numpy as np
import pywt
import scipy.linalg as linalg

def RotateImg (image, ang):
    if hasattr(image, 'shape'):
        image_center = tuple(np.array(image.shape)/2)
        shape = tuple(image.shape)
    elif hasattr(image, 'width') and hasattr(image, 'height'):
        image_center = tuple(np.array((image.width/2, image.height/2)))
        shape = (image.width, image.height)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle,1.0)
    image = np.asarray( image[:,:] )

    rotated_image = cv2.warpAffine(image, rot_mat, shape, flags=cv2.INTER_LINEAR)
    return rotated_image
    
def ChangeBrightness (img, percent):
    img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    img1[:,:,0] *= percent / 100
    img = cv2.cvColor (img1, cv2.COLOR_YCrCb2BGR)
    return img

def CropImg (image, percent):
    if hasattr(image, 'shape'):
        shape = tuple(image.shape)
    elif hasattr(image, 'width') and hasattr(image, 'height'):
        shape = (image.width, image.height)
    cropped = image[shape[0] * percent / 2:(shape[0]*(1-percent * 2)), shape[1] * percent / 2:(shape[1]*(1-percent * 2)),:]
    return cropped
    
#def normalizeImg (img, orig):
    