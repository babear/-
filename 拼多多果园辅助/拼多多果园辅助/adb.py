import os

class adb(object):
    """description of class"""

    def __init__(self, aIP):
        self.__ip = aIP
        pass

    def Connect(self):
        os.system('adb connect %s' % self.__ip)
        pass

    def GetScreenShots(self, aPath):
        os.system('adb -s %s shell screencap -p %s' % (self.__ip, aPath))
        pass

    def PullFileToComputer(self, aPhonePath,  aComputerPath):
        os.system('adb -s %s pull %s %s' % (self.__ip, aPhonePath, aComputerPath))
        pass

    def RemoveFile(self, aPhonePath):
        os.system("adb -s %s shell rm %s" % (self.__ip, aPhonePath))
        pass

    def Click(self, x, y):
        os.system('adb -s %s shell input tap %i %i' % (self.__ip, x, y))
        pass

    def PressKey(self, keycode):
        os.system('adb -s %s shell input keyevent %s' % (self.__ip, keycode))
        pass

    def PressBackKey(self):
        self.PressKey(4)
        pass

    @staticmethod
    def Devices():
        os.system('adb devices')
        pass



