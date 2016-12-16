import cv2
import numpy as np
from PIL import Image

def recognizeWatermark(watermark):
    image = Image.fromarray(watermark)
    image.load()
    
    boxes = [(0, 0, 256, 256), (256, 0, 512, 256), (0, 256, 256, 512), (256, 256, 512, 512)]
    
    images = [None] * 4
    
    for indx, box in enumerate(boxes):
        img = image.crop(box)
        images[indx] = img.load()
    
    pics = [None] * 10
    
    for i in range(10):
        pic = Image.open(str(i)+'.jpg')
        pic = pic.convert('L')
        pix = pic.load()
        pics[i] = pix
    
    pin_code = [None] * 4

    for itr, img in enumerate(images):
        norm = np.empty(10)
        for indx, pic in enumerate(pics):
            arr = np.empty([256, 256])
            for i in range(256):
                for j in range(256):
                    arr[i][j] = img[i, j] - pic[i, j]
            norm[indx] = np.linalg.norm(arr)
        pin_code[itr] = np.argmin(norm)

    return pin_code
