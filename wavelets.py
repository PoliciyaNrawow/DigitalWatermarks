import cv2
import numpy as np
import pywt
import scipy.linalg as linalg

#Generates the watermark of requested shape. The values to wtmk are placed on the main diag.
def GenerateWatermark (shape, symb):
    if (type(symb) == str):
        symb = ord(symb)
    symb = np.float32(symb)
    watermark = np.ones(shape) / 255
    watermark *= symb
    return watermark

    
#Function to apply watermark to one particular image
def TransformImage (img, word):
    #Changing colorspace to work with Y component (luminance)
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32(img) * 1.0 / 255
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
    Ui, si, Vhi = linalg.svd(dwtDom2Wtmk, full_matrices=True)
    Si = linalg.diagsvd (si, min(Ui.shape[0],Vhi.shape[0]), max(Ui.shape[1], Vhi.shape[1]))
    
    watermark = GenerateWatermark (Si.shape, word)
    #Apply watermark
    Si += watermark
    #Perform second SVD
    Uwi, swi, Vhwi = linalg.svd (Si, full_matrices=True)
    Swi = linalg.diagsvd (swi, min(Uwi.shape[0],Vhwi.shape[0]), max(Uwi.shape[1], Vhwi.shape[1]))
    #Restore chosen dwt domain with watermark embeded
    wtmkdDom = np.dot(Ui, np.dot(Swi, Vhi))

    #Getting back to dwt image
    hh = wtmkdDom
    coeffs[len(coeffs)-2] = (lh,hh,hl)
    #Perform inverse wawelet transform
    img3 = pywt.waverec2(coeffs, 'db1')
    img1[:,:,0] = img3
    #Return to the standart colorspace
    img1 = cv2.cvtColor (img1, cv2.COLOR_YCrCb2BGR)
    return img1
  
def GetSubmatrWithWatermark (img, word):
        #Changing colorspace to work with Y component (luminance)
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32 (img) * 1.0 / 255
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
    Ui, si, Vhi = linalg.svd(dwtDom2Wtmk, full_matrices=True)
    Si = linalg.diagsvd (si, min(Ui.shape[0],Vhi.shape[0]), max(Ui.shape[1], Vhi.shape[1]))
    watermark = GenerateWatermark (Si.shape, word)
    #Apply watermark
    Siw = Si + watermark
    #Perform second SVD
    Uwi, swi, Vhwi = linalg.svd (Siw, full_matrices=True)

    return (Uwi, Si, Vhwi)
    
def GetSubmatrWithoutWatermark (img):
    #Changing colorspace to work with Y component (luminance)
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32(img) * 1.0 / 255
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
    Ui, si, Vhi = linalg.svd(dwtDom2Wtmk, full_matrices=True)
    Si = linalg.diagsvd (si, min(Ui.shape[0],Vhi.shape[0]), max(Ui.shape[1], Vhi.shape[1]))
    #print (Si)
    return (Ui, Si, Vhi)

    
#A function to retireve the watermark
def RetrieveWat (inp_img, orig_img, word):
    if (inp_img.shape != orig_img.shape):
        new_inp = orig_img
        for i in range (orig_img.shape[0]):
            for j in range (orig_img.shape[1]):
                if (i < inp_img.shape[0] and  j < inp_img.shape[1]):
                    new_inp[i][j] = inp_img[i][j]
                else:
                    new_inp[i][j] = 0.0 
        inp_img = new_inp
    Uwi0, Si0, Vhwi0 = GetSubmatrWithWatermark (orig_img, word)
    Uwi, Si, Vhi = GetSubmatrWithoutWatermark (inp_img)
    D = np.dot (Uwi0, np.dot (Si, Vhwi0))
    retrWat = D - Si0
    retrWat *= 255
    sum = 0
    cnt = 0
    for i in range (retrWat.shape[0]):
        for j in range (retrWat.shape[1]):
            if (i != j):
                sum += retrWat[i][j]
                cnt += 1
    #print (sum/cnt)
    return np.uint8 (round (sum / cnt))
   
