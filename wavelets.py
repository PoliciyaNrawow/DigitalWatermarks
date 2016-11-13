import cv2
import numpy as np
import pywt
import scipy.linalg as linalg

#Function to write. No in test-mode its just generating zeroed matrix of requested shape
def GenerateWatermark (shape):
    watermark = np.zeros(shape)
    return watermark

    
#Function to apply watermark to one particular image
def TransformImage (img):
    #Changing colorspace to work with Y component (luminance)
    img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    img2 = img1[:,:,0]
    #Perform wavelet transform
    coeffs = pywt.wavedec2(img2, 'db1')
    hl=coeffs[len(coeffs)-2][2]
    hh=coeffs[len(coeffs)-2][1]
    lh=coeffs[len(coeffs)-2][0]
    #Let's work with hh matrix
    dwtDom2Wtmk = hh
    #Perform first SVD
    Ui, si, Vhi = linalg.svd(dwtDom2Wtmk)
    Si = linalg.diagsvd (si, min(Ui.shape[0],Vhi.shape[0]), max(Ui.shape[1], Vhi.shape[1]))
    
    watermark = GenerateWatermark (Si.shape)
    #Apply watermark
    Si += watermark
    #Perform second SVD
    Uwi, swi, Vhwi = linalg.svd (Si)
    Swi = linalg.diagsvd (swi, min(Uwi.shape[0],Vhwi.shape[0]), max(Uwi.shape[1], Vhwi.shape[1]))
    #Restore chosen dwt domain with watermark embeded
    wtmkdDom = np.dot(Ui, np.dot(Swi, Vhi))

    #Getting back to dwt image
    hh = wtmkdDom
    coeffs[len(coeffs)-2] = (lh,hh,hl)
    #Perform inverse wawelet transform
    img3 = pywt.waverec2(coeffs, 'db1')
    img3 = img3.astype(int)
    
    img1[:,:,0] = img3
    #Return to the standart colorspace
    img1 = cv2.cvtColor (img1, cv2.COLOR_YCrCb2BGR)
    return img1
  
def GetSubmatrWithWatermark (img):
        #Changing colorspace to work with Y component (luminance)
    img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    img2 = img1[:,:,0]
    #Perform wavelet transform
    coeffs = pywt.wavedec2(img2, 'db1')
    #hl=coeffs[len(coeffs)-2][2]
    hh=coeffs[len(coeffs)-2][1]
    #lh=coeffs[len(coeffs)-2][0]
    #Let's work with hh matrix
    dwtDom2Wtmk = hh
    #Perform first SVD
    Ui, si, Vhi = linalg.svd(dwtDom2Wtmk)
    Si = linalg.diagsvd (si, min(Ui.shape[0],Vhi.shape[0]), max(Ui.shape[1], Vhi.shape[1]))
    watermark = GenerateWatermark (Si.shape)
    #Apply watermark
    Siw = Si + watermark
    #Perform second SVD
    Uwi, swi, Vhwi = linalg.svd (Siw)

    return (Uwi, Si, Vhwi)
    
    
#A function to retireve the watermark
def RetrieveWat (inp_img, orig_img):
    Uwi0, Si0, Vhwi0 = GetSubmatrWithWatermark (orig_img)
    Uwi, Si, Vhi = GetSubmatrWithWatermark (inp_img)
    D = np.dot (Uwi0, np.dot (Si, Vhwi0))
    retrWat = D - Si0
    return retrWat 
    