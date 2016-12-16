import cv2
import numpy as np
import pywt
import scipy.linalg as linalg

#Generates the watermark of requested shape. The values to wtmk are placed on the main diag.
def GenerateWatermark (shape, symb):
    #if (type(symb) == str):
    #    symb = ord(symb)
    #symb = np.float32(symb) 
    #watermark = np.ones(shape) / 255 
    #watermark *= symb
    #print (shape)
    img = cv2.imread(symb)
    if (img.ndim > 2):
        img = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
    img = cv2.resize (img, shape)
    img = np.float32 (img) / 200
    cv2.imshow ('a', img)
    cv2.waitKey (0)
    return img

    
#Function to apply watermark to one particular image
def TransformImage (img, word):
    #Changing colorspace to work with Y component (luminance)
    if (type(img[0][0][0]) == np.uint8):
        img = np.float32(img) * 1.0 / 255
    #img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    #img2 = img1[:,:,0]
    img2 = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)

    #Perform wavelet transform
    coeffs = pywt.wavedec2(img2, 'db1')
    hl=coeffs[len(coeffs)-2][2]
    hh=coeffs[len(coeffs)-2][1]
    lh=coeffs[len(coeffs)-2][0]
#    h = coeffs[len(coeffs)-1][1]
    #Let's work with hh matrix
    hh = ApplyWtmk (hh, word)
#    hl= ApplyWtmk (hl, word)
#    lh = ApplyWtmk (lh, word)
    coeffs[len(coeffs)-2] = (lh,hh,hl)
    #Perform inverse wawelet transform
    img3 = pywt.waverec2(coeffs, 'db1')
    #img1[:,:,0] = img3
    #Return to the standart colorspace
    #img1 = cv2.cvtColor (img1, cv2.COLOR_YCrCb2BGR)
    return img3
  
def ApplyWtmk (dwtDom2Wtmk, word):
    #Perform first SVD
    Ui, si, Vhi = linalg.svd(dwtDom2Wtmk, full_matrices=True)
    Si = linalg.diagsvd (si, min(Ui.shape[0],Vhi.shape[0]), max(Ui.shape[1], Vhi.shape[1]))
#    watermark = GenerateWatermark (dwtDom2Wtmk.shape, word)   
    watermark = GenerateWatermark (Si.shape, word)
    #Apply watermark
    Si += watermark
    #Perform second SVD
    Uwi, swi, Vhwi = linalg.svd (Si, full_matrices=True)
    Swi = linalg.diagsvd (swi, min(Uwi.shape[0],Vhwi.shape[0]), max(Uwi.shape[1], Vhwi.shape[1]))
    #Restore chosen dwt domain with watermark embeded
    wtmkdDom = np.dot(Ui, np.dot(Swi, Vhi))
    #wtmkdDom = dwtDom2Wtmk + watermark;
    return wtmkdDom


def GetSubmatrWithWatermark (img, word):
        #Changing colorspace to work with Y component (luminance)
    #if (type(img[0][0][0]) == np.uint8):
        #img = np.float32 (img) * 1.0 / 255
    #img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    #img2 = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
    if (type(img[0][0]) == np.uint8):
        img = np.float32 (img) * 1.0 / 255

    #img2 = img1[:,:,0]
    #Perform wavelet transform
    coeffs = pywt.wavedec2(img, 'db1')
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
    #if (type(img[0][0][0]) == np.uint8):
    #    img = np.float32(img) * 1.0 / 255
    #img1 = cv2.cvtColor (img, cv2.COLOR_BGR2YCrCb)
    #img2 = img1[:,:,0]
    #img2 = cv2.cvtColor (img, cv2.COLOR_RGB2GRAY)
    if (type(img[0][0]) == np.uint8):
        img = np.float32 (img) * 1.0 / 255

    #Perform wavelet transform
    coeffs = pywt.wavedec2(img, 'db1')
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

    
#A function to retrieve the watermark
def RetrieveWat (inp_img, orig_img, word):
#    if (word != 1 && word != 0):
#        return np.uint8(0)
    #cv2.imshow('orig', orig_img)
    #cv2.imshow('inp', inp_img)
    print (inp_img.shape, orig_img.shape)
    if (inp_img.ndim > 2):
        inp_img = cv2.cvtColor (inp_img, cv2.COLOR_RGB2GRAY)
    if (orig_img.ndim > 2):
        orig_img = cv2.cvtColor (orig_img, cv2.COLOR_RGB2GRAY)
    if (inp_img.shape != orig_img.shape):
        print ("FUCK!")
        #new_inp = orig_img
        #for i in range (orig_img.shape[0]):
        #    for j in range (orig_img.shape[1]):
        #        if (i < inp_img.shape[0] and  j < inp_img.shape[1]):
        #            new_inp[i][j] = inp_img[i][j]
        #        else:
        #            new_inp[i][j] = 0.0 
        inp_img = cv2.resize (inp_img, orig_img.shape)
    Uwi0, Si0, Vhwi0 = GetSubmatrWithWatermark (orig_img, word)
    Uwi, Si, Vhi = GetSubmatrWithoutWatermark (inp_img)
    D = np.dot (Uwi0, np.dot (Si, Vhwi0))
#    inp_img = cv2.cvtColor (inp_img, cv2.COLOR_BGR2YCrCb) 
#    img1 = inp_img[:,:,0]
#    coeffs = pywt.wavedec2(img1, 'db1')
#    hh1 = coeffs[len(coeffs)-2][1]
#    orig_img = cv2.cvtColor (orig_img, cv2.COLOR_BGR2YCrCb)
#    img1 = orig_img[:,:,0]
#    coeffs = pywt.wavedec2(img1, 'db1')
#    hh2 = coeffs[len(coeffs)-2][1]
#    retrWat = hh1 - hh2
#    retrWat *= 255
    

    retrWat = D - Si0
    #retrWat = D
    retrWat *= 200
    cv2.imshow ('retr', retrWat)
    cv2.waitKey(0)
    #sum = 0
    #cnt = 0
    #for i in range (retrWat.shape[0]):
     #   for j in range (retrWat.shape[1]):
      #      if (abs(retrWat[i][j]-word) <=10):
       #         sum += retrWat[i][j]
        #        cnt += 1
    #print (cnt)
    #print (sum/cnt)
    return retrWat
   
