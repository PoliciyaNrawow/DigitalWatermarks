import cv2
import numpy as np
from PIL import Image

def recognizeWatermark(watermark):
    image = Image.fromarray(watermark)
    image.load()
    
    boxes = [(0, 0, 64, 64), (64, 0, 128, 64), (0, 64, 64, 128), (64, 64, 128, 128)]
    
    images = [None] * 4
    
    for indx, box in enumerate(boxes):
        img = image.crop(box)
        images[indx] = img.load()
    
    pics = [None] * 10
    
    for i in range(10):
        pic = Image.open(str(i)+'re.jpg')
        pic = pic.convert('L')
        pix = pic.load()
        pics[i] = pix
    
    
    pin_code = [None] * 4

    for itr, img in enumerate(images):
        norm = np.empty(10)
        for indx, pic in enumerate(pics):
            arr = np.empty([64, 64])
            for i in range(64):
                for j in range(64):
                    arr[i][j] = img[i, j] - pic[i, j]
            norm[indx] = np.linalg.norm(arr)
        pin_code[itr] = np.argmin(norm)
        print(norm)

    return pin_code
