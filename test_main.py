import wavelets
import cv2
import numpy as np
import attacks
import WatermarkGenerator as wat


wat1 = wat.createWatermark ([1,2,3,4])
cv2.imshow('wa', wat1)
img = cv2.imread('lena.png')
img2 = cv2.imread('3.png')
#cv2.imshow('orig', img)
#print(img)
word = '1234.png'
#print(ord(word))
#img1 = wavelets.TransformImage (img, word)
img = np.float32(img) * 1.0 / 255
#img1 = np.uint8(img1*255)
#print (img1-img)
#cv2.imshow('orig', img)
#cv2.waitKey(0)
#cv2.imshow('wtmd', img1)
#cv2.waitKey(0)
#img2 = img1
#img2 = attacks.RotateImg(img1, 5)
#img2 = attacks.ChangeBrightness(img2, 70)
#img2 = attacks.CropImg(img2, 5)
#cv2.imshow('rot', img2)
#cv2.waitKey(0)
#cv2.imwrite('attacked.tiff', np.uint8(img2*255))
#img2 = cv2.imread ('attacked.tiff')
#cv2.imshow('ph', img2)
#cv2.waitKey(0)
#img2 = np.float32(np.ones(img2.shape))
#img2 = attacks.NormalizeImg (img2, img)
cv2.imshow('kjh', img2)
wtmk = wavelets.RetrieveWat(img2, img, 'lena.png')
#sum = 0
#cnt = 0
#for i in range(wtmk.shape[0]):
    #if (wtmk[i][i] > 97.5):
        #print (wtmk[i][i])
    #for  j in range(wtmk.shape[1]):
        #if (i != j):
            #sum += wtmk[i][j]
            #cnt += 1
        #if (wtmk[i][j] > 97.5):
            #print(wtmk[i][j])

#print (sum / cnt)
#print(wtmk)
cv2.imwrite ('wtmk.png', np.uint16(wtmk))
cv2.imshow('AAAAAAAA', wtmk)
cv2.waitKey(0)




