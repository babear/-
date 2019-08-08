import os
import cv2
import numpy as np
import time
import random
from PIL import Image
import pytesseract


class Languages:
    CHS = 'chi_sim'
    CHT = 'chi_tra'
    ENG = 'eng'

def img_to_str(image_path, lang=Languages.ENG):
    return pytesseract.image_to_string(Image.open(image_path), lang)
 
#print(img_to_str('image/test2.png', lang=Languages.CHS))

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
    os.system('adb -s 127.0.0.1:62025 shell screencap -p /sdcard/pinduoduo/0.png')
    os.system('adb -s 127.0.0.1:62025 pull /sdcard/pinduoduo/0.png ./temp/%s.png' % str(id))
    os.system("adb -s 127.0.0.1:62025 shell rm /sdcard/pinduoduo/0.png")

def adb_key(keycode):
    os.system('adb shell input keyevent %s' % keycode)

def adb_backkey():
    adb_key(4)

def adb_click(x,y):
    os.system('adb shell input tap %i %i' % (x, y))

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

def liwuMatch(screen, liwuImg, i):
    matchResult = flannMatch(screen, liwuImg)
    if not matchResult is None:
        # 标记目标图位置
        cv2.polylines(screen,[np.int32(matchResult)],True,0,5,cv2.LINE_AA)

        # 标记单击点位置
        x = int(np.average(matchResult, axis =0, weights=None)[0][0])
        y = int(np.average(matchResult, axis =0, weights=None)[0][1])
        setPointFlagImage(screen, x, y)

        adb_click(x,y)

        # 保存检验图片
        cv2.imwrite('./temp/liwu_check_%s.png' % i, screen)

        return True
    else:
        return False

def closeMatch(screen, closeImg, i):
    matchResult = flannMatch(screen, closeImg)
    if not matchResult is None:
        # 标记目标图位置
        cv2.polylines(screen,[np.int32(matchResult)],True,0,5,cv2.LINE_AA)

        # 标记单击点位置
        x = int(np.average(matchResult, axis =0, weights=None)[0][0])
        y = int(np.average(matchResult, axis =0, weights=None)[0][1])
        setPointFlagImage(screen, x, y)

        adb_click(x,y)

        # 保存检验图片
        cv2.imwrite('./temp/close_check_%s.png' % i, screen)

        return True
    else:
        return False

def GetNumberOfWater(screenImg):
    numberOfWaterImg = screenImg[1605:1660 ,874:1024]
    waterNumber = pytesseract.image_to_string(numberOfWaterImg,'osd+eng')
    cv2.imwrite('./temp/NumberOfWater_%s.png' % waterNumber, numberOfWaterImg)
    return int(waterNumber[0:-1])
        
def main():
    remove_file()
    for i in range(1,70):
        get_screenshot(i)
        screen = cv2.imread('./temp/%s.png' % i, 0)
        shuihu = cv2.imread('shuihu.png', 0)
        liwu = cv2.imread('liwu.png', 0)
        close = cv2.imread('close.png', 0)
        comein = cv2.imread('comein.png', 0)
        
        waterJugPoint = flannMatch(screen, shuihu)

        if not waterJugPoint is None:
            # 标记目标图位置

            waterNumber = GetNumberOfWater(screen)
            print('water number:%i' % waterNumber)

            if waterNumber < 10:
                print('water number is less')
                break

            cv2.polylines(screen,[np.int32(waterJugPoint)],True,0,5,cv2.LINE_AA)

            # 标记单击点位置
            x = int(np.average(waterJugPoint, axis =0, weights=None)[0][0])
            y = int(np.average(waterJugPoint, axis =0, weights=None)[0][1])
            setPointFlagImage(screen, x, y)

            print('click water jug')
            adb_click(x,y)

            # 保存检验图片
            cv2.imwrite('./temp/text_check.png', screen)
            time.sleep(16)

        else:
            comein_flag = True
            while comein_flag:
                get_screenshot(i)
                screen = cv2.imread('./temp/%s.png' % i, 0)
                matchResult = flannMatch(screen, comein)

                
                if not matchResult is None:
                    comein_flag = False;
                    # 标记单击点位置
                    x = int(np.average(matchResult, axis =0, weights=None)[0][0])
                    y = int(np.average(matchResult, axis =0, weights=None)[0][1])
                    
                    print('come in pinduoduo')
                    adb_click(x,y)

                    time.sleep(5)

                else:
                    print('click back')
                    adb_backkey()
                    time.sleep(2)

            #backresult = liwuMatch(screen, liwu, i)
            #closeMatch(screen, close,i)

if __name__ == '__main__':
    main()
