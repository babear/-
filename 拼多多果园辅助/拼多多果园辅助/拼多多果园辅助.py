import os
import cv2
import numpy as np
import time
import random
from PIL import Image
import adb
import ImageMatch
import PinDuoDuo

androidAdb = adb.adb('127.0.0.1:62001')

def get_screenshot(id):
    androidAdb.GetScreenShots('/sdcard/pinduoduo/0.png')
    androidAdb.PullFileToComputer('/sdcard/pinduoduo/0.png', './temp/%s.png' % str(id))
    androidAdb.RemoveFile('/sdcard/pinduoduo/0.png')
    pass

def remove_file():
    files = os.listdir('./temp/')
    for file in files:
        os.remove('./temp/' + file)



def main():
    get_screenshot(0)
    screen = cv2.imread('./temp/0.png', 0)
    shuihu = cv2.imread('shuihu.png', 0)
    
    matchResult = ImageMatch.FlannMatch(screen, shuihu)

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

        pass
    pass

def test():
    androidAdb = adb.adb('127.0.0.1:62001')
    androidAdb.Connect()

    pinDuoDuo = PinDuoDuo.PinDuoDuoTask(androidAdb)
    pinDuoDuo.RemoveTempFiles();
    #pinDuoDuo.Task_SeeGoods()
    pinDuoDuo.Task_DailyGetWater()
    pass

if __name__ == '__main__':
    # main()
    test()

