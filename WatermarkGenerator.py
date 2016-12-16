def createWatermark(pin_code):
    img = np.zeros((512,512,3), np.uint8)

    # Write some Text
    font = cv2.FONT_HERSHEY_SIMPLEX

    retval, baseline = cv2.getTextSize(pin_code[0], font, 6, 6) 
    cv2.putText(img,pin_code[0], (int(img.shape[0] / 4 - retval[0] / 2), int(img.shape[1] / 4 + retval[1] / 2)), font, 6, (255,255,255), 6, False)

    retval, baseline = cv2.getTextSize(pin_code[1], font, 6, 6) 
    cv2.putText(img,pin_code[1], (int(3 * img.shape[0] / 4 - retval[0] / 2), int(img.shape[1] / 4 + retval[1] / 2)), font, 6, (255,255,255), 6, False)

    retval, baseline = cv2.getTextSize(pin_code[2], font, 6, 6) 
    cv2.putText(img,pin_code[2], (int(img.shape[0] / 4 - retval[0] / 2),int(3 * img.shape[1] / 4 + retval[1] / 2)), font, 6, (255,255,255), 6, False)

    retval, baseline = cv2.getTextSize(pin_code[3], font, 6, 6) 
    cv2.putText(img,pin_code[3], (int(3 * img.shape[0] / 4 - retval[0]/2),int(3 * img.shape[1] / 4 + retval[1] / 2)), font, 6, (255,255,255), 6, False)

    #Save image
    cv2.imwrite("out.jpg", img)
    
    return img