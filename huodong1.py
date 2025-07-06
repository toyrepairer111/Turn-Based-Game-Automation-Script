import logging
import random
import threading
from datetime import datetime

import pyautogui

from Thread_function import detect_combat_chumo
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, bb_dead, detect_combat_or_not,  move_window2
from chumo import Daily_chumo
from threading import Event
from shimen import Daily_shimen

class Menpai:
    @staticmethod
    def menpai(level):
        while True:
            current_hour = datetime.now().hour
            if current_hour >= 21:
                break
            else:
                print('等待十分钟')
                time.sleep(600)
        Daily_shimen.press_esc()
        Daily_chumo.leave_team()
        stop_event = Event()
        t1 = threading.Thread(target=Daily_chumo.auto_incense, args=(stop_event,))
        t1.start()
        t2 = threading.Thread(target=detect_combat_chumo, args=(stop_event,))
        t2.start()
        t3 = threading.Thread(target=Daily_chumo.auto_f9, daemon=True)
        t3.start()
        click_time =True
        cnt = 0
        press_button('alt', 'v')
        time.sleep(1)
        text_ocr.ocr_target(region=(599, 590, 825 - 599, 654 - 590), text='创建队伍', click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(181, 169, 174, 467), text='全部队伍', click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(436, 214, 377, 365), text='门派论剑', click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(606, 357, 811 - 606, 510 - 357,), text='开始匹配', click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(275,320, 460,247), text='挑战', click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(306, 277, 469,442), text='开始匹配', click_or_not=True)
        while True:
            time.sleep(1)
            ren_shu = text_ocr.ocr_target(region=(211, 504, 386 - 211, 570 - 504), text=None, click_or_not=False)
            if any('级' in item for item in ren_shu):
                print('匹配成功，开始门派任务')
                time.sleep(1)
                press_button('alt', 'v')
                break
        press_button('alt', 'y'), time.sleep(1.5)
        for _ in range(2):
            text_ocr.ocr_target(region=(179, 444, 706, 236), text='门派', click_or_not=True)
        Daily_shimen.moving()
        while True:
            if text_ocr.ocr_target(region=(351, 400, 577 - 364, 557 - 400), text='我要参加', click_or_not=True):
                press_button('alt', 'y')
                break
            time.sleep(1)
        for _ in range(2):
            Daily_shimen.press_esc()
            time.sleep(1)
        while True:
            R1 = text_ocr.moving_detect(region=(51,48,52,42))
            time.sleep(1)
            R2 = text_ocr.moving_detect(region=(51,48,52,42))
            if detect_combat_or_not() is False:
                R1 = text_ocr.moving_detect()
                time.sleep(1)
                R2 = text_ocr.moving_detect()
                print(f"是否需要点击门派导航:{click_time}")
                if text_ocr.ocr_target_text(region=(181,171,687,502), text='恭喜你们'):
                    time.sleep(0.5)
                    text_ocr.ocr_target(region=(181, 171, 687, 502), text='恭喜你们',click_or_not=True)
                    click_time = True
                    cnt = 0
                if text_ocr.ocr_target_text(region=(181, 171, 687, 502), text='胜败'):
                    time.sleep(0.5)
                    text_ocr.ocr_target(region=(181, 171, 687, 502), text='胜败', click_or_not=True)
                    click_time = True
                    cnt = 0
                if click_time :
                    while True:
                        if text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='门派论剑', click_or_not=True):
                            time.sleep(1)
                            text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='门派论剑',
                                                click_or_not=True)
                            break
                    print('继续下一关门派')
                    click_time = False
                    cnt = 0
                if text_ocr.ocr_target(region=(351, 400, 448,129), text=F'{level}', click_or_not=True):
                    print(f'门派选择{level}星级')
                    cnt = 0
            if R1==R2 and detect_combat_or_not() == False:
                cnt += 1
                time.sleep(1)
                print(f'现在计数器为：{cnt}')
                if cnt >15:
                    break_text =text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text=None, click_or_not=False)
                    print(f'break_text:{break_text}')
                    if any('门派' or '门派论剑' or '论剑' not in item for item in break_text) and detect_combat_or_not() == False:
                            print('门派论剑结束，退出')
                            stop_event.set()
                            break
            else:
                if detect_combat_or_not():
                    print('战斗中')
                    time.sleep(3)
                    click_time = True
                else:
                    Daily_shimen.moving()
                    time.sleep(0.5)
                    click_time = False

if __name__ == '__main__':
    move_window('风驰电掣')
    t3 = threading.Thread(target=Daily_chumo.auto_f9, daemon=True)
    t3.start()
    Menpai.menpai(10)




