import wavelets
import cv2
import numpy as np
import attacks

img = cv2.imread('2z.jpg')
cv2.imshow('orig', img)
#print(img)
word = 2
#print(ord(word))
img1 = wavelets.TransformImage (img, word)
img = np.float32(img) * 1.0 / 255
#img1 = np.uint8(img1*255)
#print (img1-img)
#cv2.imshow('orig', img)
#cv2.waitKey(0)
cv2.imshow('wtmd', img1)
#cv2.waitKey(0)
img2 = img1
img2 = attacks.RotateImg(img1, 5)
img2 = attacks.ChangeBrightness(img2, 120)
img2 = attacks.CropImg(img2, 5)
cv2.imshow('rot', img2)
cv2.waitKey(0)
#img2 = np.float32(np.ones(img2.shape)*100)
#img2 = attacks.NormalizeImg (img2, img)
wtmk = wavelets.RetrieveWat(img2, img, word)
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
print(wtmk)


