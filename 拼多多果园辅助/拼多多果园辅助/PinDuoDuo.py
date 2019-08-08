import cv2
import ImageMatch
import ImgHelper

class PinDuoDuoTask(object):

    def __init__(self, adb):
        self.__adb = adb
        self.__kettleImg = cv2.imread('Kettle.png', 0)
        self.__bringWaterDropletsImg = cv2.imread('BringWaterDroplets.png', 0)
        self.__seeGoodsFlagImg = cv2.imread('SeeGoodsFlag.png', 0)
        pass

    def GetScreenShot(self, fileName):
        self.__adb.GetScreenShots('/sdcard/pinduoduo/0.png')
        self.__adb.PullFileToComputer('/sdcard/pinduoduo/0.png', './temp/%s.png' % str(fileName))
        self.__adb.RemoveFile('/sdcard/pinduoduo/0.png')
        pass

    def UpdateScreenImg(self, fileName):
        self.__screenImg = cv2.imread('./temp/%s.png' % str(fileName), 0)
        return self.__screenImg
        pass

    def UpdateScreenFileName(self):
        if(self.__fileName == None):
            self.__fileName = 0
            pass
        else:
            self.__fileName = self.__fileName + 1
            pass

        return self.__fileName
        pass

    def Task_SeeGoods(self):
        print("Start see goods task.")

        fileName = self.UpdateScreenFileName()
        self.GetScreenShot(fileName)
        self.UpdateScreenImg(fileName)

        matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__bringWaterDropletsImg)
        if matchResult != None:

            ImgHelper.SetPointFlagImage(self.__screenImg, )

            matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__seeGoodsFlagImg)
            if matchResult != None:
                pass
            else:
                print("Can't find the SeeGoodsFlagImg.")
                pass

            pass
        else:
            print("Can't find the BringWaterDropletsImg.")
            pass

        print("End see goods task.");
        pass
