import wavelets
import cv2

img = cv2.imread('2z.jpg')
cv2.imshow('orig', img)
img1 = wavelets.TransformImage (img)
cv2.imshow('orig', img)
cv2.imshow('wtmd', img1)

wtmk = wavelets.RetrieveWat(img1, img)
print(wtmk)



