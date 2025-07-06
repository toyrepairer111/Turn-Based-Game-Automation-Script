import pyautogui

from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, wen_jian
from text_ocr_file import text_ocr
from shimen import Daily_shimen
import random

def use_xiang():
    if text_ocr.detect_pic('xiang', region=(900, 93, 1028 - 900, 148 - 93)):
        print('已使用香')
    else:
        press_button('alt','e')
        time.sleep(0.7)
        if locate_pos_click3('xiang1',right_button=True)is not False:
            human_like_move(275 + random.uniform(-30, 30), 620 + random.uniform(-30, 30))
            press_button('alt', 'e')
            print('上香中，拜佛')
        else:
            pyautogui.press('F6')
            time.sleep(0.7)
            locate_pos_click3('xiang1')
            time.sleep(0.7)
            text_ocr.ocr_target(region=(370,511,196,112),text='信誉购买',click_or_not=True)
            Daily_shimen.press_esc()
            time.sleep(0.7)
            press_button('alt', 'e')
            time.sleep(0.7)
            locate_pos_click3('xiang1',right_button=True)
            human_like_move(275 + random.uniform(-30, 30), 620 + random.uniform(-30, 30))
            Daily_shimen.press_esc()