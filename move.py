import time

import pyautogui
import random

pyautogui.FAILSAFE = False
while True:
    delay = random.randint(2, 20)
    disx = random.randint(-400, 400)
    disy = random.randint(-400, 400)
    time.sleep(delay)
    pyautogui.moveRel(disx, disy, duration=0.1)  # 根据当前位置, 相对移动鼠标指针  durtion移动时间
