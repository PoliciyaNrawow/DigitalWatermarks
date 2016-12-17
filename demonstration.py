import numpy as np
import cv2
import wavelets
import attacks
import WatermarkGenerator as wat
import sys
import WatermarkRecognizer as rec

word = sys.argv[1:]
img = cv2.imread('lena.png')
cv2.imshow('original image', img)
print (word)
wtmk = wat.createWatermark (word)
cv2.imshow ('watermark', wtmk)
wtmkd_img = wavelets.TransformImage (img, word)

cv2.imshow ('watermarked image', wtmkd_img)
cv2.waitKey (0)

print ("Trying some attacks")

rot_img = attacks.RotateImg (wtmkd_img, 5)
cv2.imshow ('rotated image', rot_img)
out_wtmk = wavelets.RetrieveWat (rot_img, wtmkd_img, word)

detected_word = rec.recognizeWatermark (out_wtmk)
message = 'retr wtmk: ' + str(detected_word)
print(message)
cv2.imshow (message, out_wtmk)
cv2.waitKey (0)

