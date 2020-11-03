

import win32gui
import time
import psutil
import win32process
import cv2, pyautogui
import numpy as np
import imagehash
from PIL import Image
from datetime import datetime
from log import configure_logger


class GameWatcher:
    def __init__(self):
        self.start = 0
        self.last_screenshot = None
        self.log = configure_logger("GameWatcher")

    def take_screenshot(self, save=True):
        now = datetime.now()
        #current_dir = self.get_activity_dir()
        filename = "photo" + "/" + now.strftime("%H-%M-%S.png")
        image = pyautogui.screenshot() 
        image = cv2.cvtColor(np.array(image), 
                            cv2.COLOR_RGB2BGR) 
        if(save):
            cv2.imwrite(filename , image, [cv2.IMWRITE_PNG_COMPRESSION, 9]) 
        return filename

    def get_current_activity(self):
        w=win32gui
        w.GetWindowText (w.GetForegroundWindow())
        pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
        current_activity_name = psutil.Process(pid[-1]).name()
        return current_activity_name


    def main_loop(self):
        while True:
            time.sleep(3)
            screenshot = self.take_screenshot()
            if(self.last_screenshot is not None):
                hash0 = imagehash.average_hash(Image.open(screenshot))
                hash1 = imagehash.average_hash(self.last_screenshot)
                print("Hash are {}".format(hash0 - hash1))
            self.last_screenshot = Image.open(screenshot)

    

    