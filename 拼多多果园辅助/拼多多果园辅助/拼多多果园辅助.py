import os
import cv2
import numpy as np
import time
import random
from PIL import Image

def connect():
    while True:
        print('---------------------------------')
        print('0. exit')
        print('1. devices')
        print('2. connect 127.0.0.1:62001')
        print('---------------------------------')
        cmd = input('press input the number:')

        if cmd == '0':
            break
        elif cmd == '1':
            os.system('adb devices')
        elif cmd == '2':
            os.system('adb connect 127.0.0.1:62001')

        cmd = input('Return to the previous menu(y) or continue(n):')

        if cmd == 'y':
            break

def get_screenshot(id):
    os.system('adb -s 127.0.0.1:62001 shell screencap -p /sdcard/pinduoduo/0.png')
    os.system('adb -s 127.0.0.1:62001 pull /sdcard/pinduoduo/0.png ./temp/%s.png' % str(id))
    os.system("adb -s 127.0.0.1:62001 shell rm /sdcard/pinduoduo/0.png")

def remove_file():
    files = os.listdir('./temp/')
    for file in files:
        os.remove('./temp/' + file)

def setPointFlagImage(img_gray, x_center, y_center):
    img_gray = cv2.circle(img_gray, (x_center, y_center), 9, 255, -1)
    img_gray = cv2.circle(img_gray, (x_center, y_center), 6, 0, -1)
    img_gray = cv2.circle(img_gray, (x_center, y_center), 3, 255, -1)
    return img_gray

def flannMatch(parentImg, childImg):
    MIN_MATCH_COUNT=10 #设置最低匹配数量为10
    sift=cv2.xfeatures2d.SIFT_create() #创建sift检测器
    kp1,des1=sift.detectAndCompute(childImg,None) 
    kp2,des2=sift.detectAndCompute(parentImg,None)
    #创建设置FLAAN匹配
    FLANN_INDEX_KDTREE=0
    index_params=dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params=dict(checks=50)
    flann=cv2.FlannBasedMatcher(index_params,search_params)
    mathces=flann.knnMatch(des1,des2,k=2)
    good=[]
    #过滤不合格的匹配结果，大于0.7的都舍弃
    for m,n in mathces:
        if m.distance<0.7*n.distance:
            good.append(m)
    #如果匹配结果大于10，则获取关键点的坐标，用于计算变换矩阵
    if len(good)>MIN_MATCH_COUNT:
        src_pts=np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts =np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    
        #计算变换矩阵和掩膜
        M,mask=cv2.findHomography(src_pts,dst_pts,cv2.RANSAC,10.0)
        matchesMask=mask.ravel().tolist()
        #根据变换矩阵进行计算，找到小图像在大图像中的位置
        h,w=childImg.shape
        pts=np.float32([[0,0],[0,h-1],[w-1,h-1],[w-1,0]]).reshape(-1,1,2)
        dst=cv2.perspectiveTransform(pts,M)
        return dst
    else:
        matchesMask=None
        return None

def main():
    get_screenshot(0)
    screen = cv2.imread('./temp/0.png', 0)
    shuihu = cv2.imread('shuihu.png', 0)
    
    matchResult = flannMatch(screen, shuihu)

    if matchResult != None:
        # 标记目标图位置
        cv2.polylines(screen,[np.int32(matchResult)],True,0,5,cv2.LINE_AA)

        # 标记单击点位置
        x = int(dst[2][0][0]) - 50
        y = int(dst[2][0][1])
        setPointFlagImage(screen, x, y)

        # 单击
        cmd = ('adb shell input tap %i %i' % (x, y))
        os.system(cmd)

        # 保存检验图片
        cv2.imwrite('./temp/text_check.png', screen)


if __name__ == '__main__':
    main()

