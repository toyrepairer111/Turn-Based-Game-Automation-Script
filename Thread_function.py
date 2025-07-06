import os
import time
import random
from io import BytesIO

import numpy as np
from PIL import Image
import pyautogui
from main import detect_combat_or_not, human_like_move, press_button
from text_ocr_file import text_ocr


def auto_guozi(stop_event):
    while not stop_event.is_set():
        time.sleep(3)
        try:
            if text_ocr.ocr_target(region=(878,650,996-878,756-650), text='使用', click_or_not=True):
                    time.sleep(180)
        except Exception as e:
            pass

def detect_combat_chumo(stop_event):
    cnt = 1
    while not stop_event.is_set():
        try:
            time.sleep(0.7)
            cnt += 1
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, 'picture', "huihe.png")
            box = pyautogui.locateOnScreen(
                image_path,
                region=(655, 47, 253, 125),
                confidence=0.7
            )
            if box:
                click_timing = True
                combat_click_over = text_ocr.ocr_target(region=(855, 150, 146, 328), text=None, click_or_not=False)
                time.sleep(1)
                if any('返回' in item for item in combat_click_over):
                    continue
                elif any('技能' or '神技' in item for item in combat_click_over) and click_timing:
                    ren_shu = text_ocr.ocr_target(region=(206, 222, 256, 360), text=None, click_or_not=False)
                    if any('级' in item for item in ren_shu):
                        time.sleep(20)
                        continue
                    if detect_combat_or_not():
                        human_like_move(313, 276)
                        pyautogui.press('F2')
                        pyautogui.click(313 + random.uniform(-3, 3), 276 + random.uniform(-3, 3), button='Left')
                        time.sleep(0.2)
                        pyautogui.click(button='Right')
                        human_like_move(313 + random.uniform(-30, 30), 276 + random.uniform(-30, 30))
                        time.sleep(1.2)
                        combat_click_over = text_ocr.ocr_target(region=(855, 150, 146, 328), text=None,
                                                                click_or_not=False)
                        if any('技能' or '神技' in item for item in combat_click_over):
                            press_button('alt', 'q')
                            time.sleep(0.5)
                            press_button('alt', 'q')

                    else:
                        if detect_combat_or_not():
                            press_button('alt', 'q')
                            time.sleep(0.5)
                            press_button('alt', 'q')
                else:
                    click_timing = True
            if cnt % 500 == 0:
                print('更新战斗回合数')
                press_button('ctrl', 'a')
        except Exception as e:
            pass