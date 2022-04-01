from ppadb.client import Client as AdbClient
import time
import cv2
import numpy as np

class Action:
    def __init__(self, device):
        self.device = device

    def __cmd(self, id):
        self.device.shell(f'input keyevent {id}')
        time.sleep(0.1)

    def Enter(self):
        """ 确认按键
        """
        self.__cmd(66)

    def Home(self):
        self.__cmd(3)

    def Back(self):
        self.__cmd(4)
    
    def TurnOn(self):
        """ 打开或关闭屏幕
        """
        self.__cmd(26)

    def Tap(self, xy, sleep = 0):
        self.device.shell(f"input tap {xy[0]} {xy[1]}")
        time.sleep(sleep)

class Screen:
    def __init__(self, device):
        self.device = device
    
    def ScreenCap(self):
        """ 抓取屏幕图像

        Returns:
            np.array: 图像
        """
        result = self.device.screencap()
        encoded_buf = np.frombuffer(result, dtype = np.uint8)
        bgr_img = cv2.imdecode(encoded_buf, cv2.IMREAD_COLOR)
        return bgr_img

def run():
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.devices()[0]
    action = Action(device)
    screen = Screen(device)

    action.TurnOn()# on or off
    action.Home()
    action.Tap((140, 229), sleep = 2)

    bgr_img = screen.ScreenCap()

    cv2.imwrite('screen.png', bgr_img)
    cv2.imshow('img', bgr_img)
    cv2.waitKey(0)

if __name__ == "__main__":
    run()