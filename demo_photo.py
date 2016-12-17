import wavelets
import cv2
import numpy as np
import WatermarkGenerator as wat
import sys
import WatermarkRecognizer as rec


word = sys.argv[1:]
wat_img = cv2.imread ('photo.png')
img = cv2.imread ('lena.png')
out_wtmk = wavelets.RetrieveWat (wat_img, img, word)

mess = 'Recognized watermark: ' + str (rec.recognizeWatermark (out_wtmk))
print(mess)
cv2.imshow ('photo of an image', wat_img)
cv2.imshow ('original image', img)
cv2.imshow (mess, out_wtmk)
cv2.waitKey(0)
