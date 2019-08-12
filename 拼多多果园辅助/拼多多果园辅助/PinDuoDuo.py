import cv2
import ImageMatch
import ImgHelper
import time
import os
import pytesseract

class PinDuoDuoTask(object):

    def __init__(self, adb):
        self.__adb = adb
        self.__kettleImg = cv2.imread('Img/Kettle.png', 0)
        self.__bringWaterDropletsImg = cv2.imread('Img/BringWaterDroplets.png', 0)
        self.__seeGoodsFlagImg = cv2.imread('Img/SeeGoodsFlag.png', 0)
        self.__goToFinishImg = cv2.imread('Img/GoToFinish.png', 0)
        self.__dailyGetWaterFlagImg = cv2.imread('Img/DailyGetWaterFlag.png', 0)
        self.__verifyDailyGetWater = cv2.imread('Img/VerifyDailyGetWater.png', 0)
        self.__screenName = None
        self.__tempFolder = './temp/'
        pass

    def RemoveTempFiles(self):
        files = os.listdir(self.__tempFolder)
        for file in files:
            os.remove(self.__tempFolder + file)
            pass
        pass

    def UpdateScreenFileName(self):
        if self.__screenName is None:
            self.__screenName = 0
            pass
        else:
            self.__screenName = self.__screenName + 1
            pass

        return self.__screenName
        pass

    def GetScreenShot(self, fileName):
        self.__adb.GetScreenShots('/sdcard/pinduoduo/0.png')
        self.__adb.PullFileToComputer('/sdcard/pinduoduo/0.png', os.path.join(self.__tempFolder, '%s.png' % str(fileName)))
        self.__adb.RemoveFile('/sdcard/pinduoduo/0.png')
        pass

    def GetScreenImg(self, fileName):
        self.__screenImg = cv2.imread(os.path.join(self.__tempFolder, '%s.png' % str(fileName)), 0)
        return self.__screenImg
        pass

    def UpdateScreenImg(self):
        screenName = self.UpdateScreenFileName()
        self.GetScreenShot(screenName)
        self.GetScreenImg(screenName)
        pass

    def WriteCheckImag(self, fileName, img):
        cv2.imwrite(os.path.join(self.__tempFolder, '%s_check.png' % str(fileName)), img)
        pass

    def WriteNumberOfWaterImg(self, fileName, img):
        cv2.imwrite(os.path.join(self.__tempFolder, 'NumberOfWater_%s.png' % str(fileName)), img)
        pass

    def Task_SeeGoods(self):
        print("Start see goods task.")

        self.UpdateScreenImg()
        matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__bringWaterDropletsImg)
        if not matchResult is None:

            # 找到领水滴图标
            x,y = ImageMatch.GetMatchResultCentralPoint(matchResult)
            self.__adb.Click(x, y)
            time.sleep(1)

            self.UpdateScreenImg()
            matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__seeGoodsFlagImg)
            if not matchResult is None:
                y = ImageMatch.GetMinY(matchResult)
                x = ImageMatch.GetMaxX(matchResult)

                img = self.__screenImg[y: y + 120, x: self.__screenImg.shape[1] - 1]
                matchResult = ImageMatch.FlannMatch(img, self.__goToFinishImg)
                if not matchResult is None:
                    img_x, img_y = ImageMatch.GetMatchResultCentralPoint(matchResult)
                    self.__adb.Click(x + img_x, y + img_y)
                    time.sleep(3)
                    time.sleep(60)
                    self.__adb.PressBackKey()
                    time.sleep(1)
                    self.__adb.Click(x + img_x, y + img_y)
                    time.sleep(0.5)
                    self.__adb.PressBackKey()
                    time.sleep(0.5)
                    self.__adb.PressBackKey()
                    time.sleep(0.5)
                    self.__adb.PressBackKey()
                    time.sleep(0.5)
                    pass
                else:
                    pass
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

    def Task_DailyGetWater(self):
        print("Start daily get water task.")

        self.UpdateScreenImg()
        matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__bringWaterDropletsImg)
        if not matchResult is None:

            # 找到领水滴图标
            x,y = ImageMatch.GetMatchResultCentralPoint(matchResult)
            self.__adb.Click(x, y)
            time.sleep(1)

            self.UpdateScreenImg()
            matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__dailyGetWaterFlagImg)
            if not matchResult is None:
                y = ImageMatch.GetMinY(matchResult)
                x = ImageMatch.GetMaxX(matchResult)

                img = self.__screenImg[y: y + 120, x: self.__screenImg.shape[1] - 1]
                matchResult = ImageMatch.FlannMatch(img, self.__goToFinishImg)
                if not matchResult is None:
                    img_x, img_y = ImageMatch.GetMatchResultCentralPoint(matchResult)
                    self.__adb.Click(x + img_x, y + img_y)
                    time.sleep(1)

                    self.UpdateScreenImg()
                    matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__verifyDailyGetWater)
                    if not matchResult is None:
                        verify_x, verify_y = ImageMatch.GetMatchResultCentralPoint(matchResult)

                        self.__adb.Click(verify_x, verify_y)
                        time.sleep(0.5)
                        self.__adb.PressBackKey()
                        time.sleep(0.5)
                        pass
                    else:
                        pass
                    pass
                else:
                    pass

                pass
            else:
                print("Can't find the DailyGetWaterFlag.")
                pass

            pass
        else:
            print("Can't find the BringWaterDropletsImg.")
            pass

        print("End daily get water task.");
        pass

    def Task_AutoWatering(self):
        print("Start auto watering task.")

        self.UpdateScreenImg()
        matchResult = ImageMatch.FlannMatch(self.__screenImg, self.__kettleImg)
        if not matchResult is None:
            numberOfWaterImg = self.__screenImg[1605:1660 ,874:1024]
            self.WriteNumberOfWaterImg(waterNumber, numberOfWaterImg)
            waterNumber = pytesseract.image_to_string(numberOfWaterImg,'osd+eng')
            waterNumber = int(waterNumber[0:-1])

            if waterNumber < 10:
                print('water number is less')
                return
            else:
                x, y = ImageMatch.GetMatchResultCentralPoint(matchResult)
                self.__adb.Click(x, y)
                time.sleep(16)
                pass
            pass
        else:
            print("Can't find the kettle.")
            pass

        print("Start auto watering task.")
        pass
