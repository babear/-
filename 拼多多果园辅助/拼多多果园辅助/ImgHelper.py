import cv2

def SetPointFlagImage(img_gray, x_center, y_center):
    img_gray = cv2.circle(img_gray, (x_center, y_center), 9, 255, -1)
    img_gray = cv2.circle(img_gray, (x_center, y_center), 6, 0, -1)
    img_gray = cv2.circle(img_gray, (x_center, y_center), 3, 255, -1)
    return img_gray
