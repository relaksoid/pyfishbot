import pyautogui
import typing as t
import time
import cv2
import mss
import numpy as np
import random
from mss.windows import MSS as mss

from constants import TEMPLATES_DIR


class PyFishBot:

    def __init__(self, top=0, left=0, width=1920, height=1080):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.monitor = {"top": self.top, "left": self.left, "width": self.width, "height": self.height}
        self.templates = self.load_templates()
        self.templates_height, self.templates_width, _ = self.templates[0].shape
        self.corc_middle_point = (self.templates_height // 2, self.templates_width // 2)

    def load_templates(self) -> t.List:
        return [cv2.imread(str(file_path)) for file_path in TEMPLATES_DIR.iterdir() if file_path.is_file()]

    def run(self):
        time.sleep(3)
        print('Start fishing')
        with mss() as sct:
            while True:
                time.sleep(random.uniform(1, 2.5))
                pyautogui.press(['1'])
                self.start_fishing(sct=sct)

    def start_fishing(self, sct):
        time.sleep(random.uniform(2,4))  # w8 while corc is down
        prev_corc_mid_point = None
        while True:
            img = np.array(sct.grab(self.monitor))[:,:,:3]
            max_cor = -1
            corc_location = (0, 0)
            for template in self.templates:
                matched = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
                _, correlation, _, location = cv2.cv2.minMaxLoc(matched)
                if correlation > max_cor:
                    corc_location = location
            corc_middle_point = \
                corc_location[1] + self.corc_middle_point[0], corc_location[0] + self.corc_middle_point[1]
            if prev_corc_mid_point is not None:
                if (abs(prev_corc_mid_point[0] - corc_middle_point[0])) > 5 or (abs(prev_corc_mid_point[1] - corc_middle_point[1])) > 5:
                    print('catch')
                    time.sleep(random.uniform(0.2, 0.4))
                    pyautogui.click(corc_middle_point[1], corc_middle_point[0])
                    return
            prev_corc_mid_point = corc_middle_point
