

import win32gui, os
import time
import psutil
import win32process
import cv2, pyautogui
import numpy as np
import imagehash
import json
from PIL import Image
from datetime import datetime
from log import configure_logger


class GameWatcher:
    def __init__(self):
        self.start = 0
        self.SECONDS_BY_PASS = 5
        self.HASH_THRESHOLD = 1
        self.last_screenshot = None
        self.log = configure_logger("GameWatcher")
        self.WHITELIST_FILENAME = "whitelist.txt"
        self.HOURS_TIME_FILENAME = "played.json"
        self.played_games = {}
        try:
            self.played_games = json.load(open(self.HOURS_TIME_FILENAME))
        except Exception as e:
            pass

    def no_exe_name(self, name):
        return name.replace('.exe','')

    def take_screenshot(self, activity, save=True):
        now = datetime.now()
        #current_dir = self.get_activity_dir()
        folder_name = self.no_exe_name(activity)
        folder = "{}/{}".format("photo", folder_name)
        filename = "{}/{}".format(folder, now.strftime("%Y-%m-%d-%H-%M-%S.png"))
        try:
            os.makedirs(folder)
        except Exception as e:
            pass
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

    def is_whitelisted(self, activity):
        is_whitelisted = False
        with open(self.WHITELIST_FILENAME) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            is_whitelisted = activity in content
        return is_whitelisted

    def write_played(self):
        self.log.debug("Writing current activity to file")
        json.dump(self.played_games, open(self.HOURS_TIME_FILENAME,'w'))

    def main_loop(self):
        while True:
            before_sleep = datetime.now()
            time.sleep(self.SECONDS_BY_PASS)
            current_activity = self.get_current_activity()
            is_whitelisted = self.is_whitelisted(current_activity)
            self.log.info("Current activity is [{}], is Whitelisted[{}]".format(current_activity, is_whitelisted))
            if(is_whitelisted):
                seconds_passed = int(round((datetime.now() - before_sleep).seconds))
                if(current_activity not in self.played_games):
                    self.played_games[current_activity] = seconds_passed
                else:
                    self.played_games[current_activity] += seconds_passed
                self.write_played()
                screenshot = self.take_screenshot(current_activity)
                new_screenshot_is_saved = True
                if(self.last_screenshot is not None):
                    hash0 = imagehash.average_hash(Image.open(screenshot))
                    hash1 = imagehash.average_hash(self.last_screenshot)
                    hash_difference = hash0-hash1
                    self.log.debug("Hash difference is {}".format(hash_difference))
                    if(not hash_difference > self.HASH_THRESHOLD):
                        os.remove(screenshot)
                        new_screenshot_is_saved = False
                if(new_screenshot_is_saved):
                    self.last_screenshot = Image.open(screenshot)

game_watcher = GameWatcher()
game_watcher.main_loop()

    

    