import logging
import os
import random

import pyautogui
import asyncio

from Thread_function import detect_combat_chumo, auto_guozi
from chumo import Daily_chumo
from shimen import Daily_shimen
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, wen_jian, \
    detect_combat_no_async, detect_combat_or_not
import threading
from threading import Event


class Xuanshang_chumo:
    @staticmethod
    def chumo():
        stop_event = Event()
        t2 = threading.Thread(target=detect_combat_chumo, args=(stop_event,))
        t2.start()
        press_button('alt', 'v')
        time.sleep(2)
        text_ocr.ocr_target(region=(204, 180, 353 - 204, 539 - 180), text='除魔', click_or_not=True)
        time.sleep(2)
        text_ocr.ocr_target(region=(596, 562, 239, 106), text='开始匹配', click_or_not=True)
        while True:
            pi_pei_zhong = text_ocr.ocr_target(region=(201, 538, 360 - 201, 630 - 538), text=None, click_or_not=False)
            if any('匹配' in item for item in pi_pei_zhong):
                print('匹配队友中，请等待')
                print(pi_pei_zhong)
                time.sleep(1)
            else:
                print('匹配成功，开始除魔任务')
                press_button('alt', 'v')
                guaji_cnt = 0
                guaji_status = False
                move_cnt =0
                while True:
                    time.sleep(1)
                    if detect_combat_or_not():
                        guaji_status = False
                        break
                    if not text_ocr.move_or_not():
                        guaji_cnt += 1
                        print(f'挂机{guaji_cnt}')
                    if guaji_cnt >= 20:
                        Daily_chumo.leave_team()
                        guaji_status = True
                        print('重新匹配')
                        break
                    if text_ocr.move_or_not():
                        move_cnt += 1
                        if move_cnt >= 3:
                            guaji_status = False
                            break
                if guaji_status:
                    continue
                elif not guaji_status:
                    break

        times = 0
        combat_status = True
        while True:
            time.sleep(5)
            if detect_combat_or_not() and combat_status == True:
                press_button('ctrl', 'a')
                times += 1
                print(f'第{times}次除魔')
                combat_status = False
                if times >= 20:
                    print('完成除魔')
                    stop_event.is_set()
                    break
            if detect_combat_or_not() == False:
                combat_status = True
            if detect_combat_or_not():
                combat_status = False
        while True:
            time.sleep(5)
            if not detect_combat_or_not():
                Daily_chumo.leave_team()
                press_button('F1', None)

class Xuanshang_fengyao:
    @staticmethod
    def fengyao():
        stop_event = Event()
        t2 = threading.Thread(target=detect_combat_chumo, args=(stop_event,))
        t2.start()
        press_button('alt', 'v')
        time.sleep(2)
        text_ocr.ocr_target(region=(204, 180, 353 - 204, 539 - 180), text='降妖', click_or_not=True)
        time.sleep(2)
        text_ocr.ocr_target(region=(596, 562, 239, 106), text='开始匹配', click_or_not=True)
        while True:
            pi_pei_zhong = text_ocr.ocr_target(region=(201, 538, 360 - 201, 630 - 538), text=None, click_or_not=False)
            if any('匹配' in item for item in pi_pei_zhong):
                print('匹配队友中，请等待')
                print(pi_pei_zhong)
                time.sleep(1)
            else:
                print('匹配成功，开始悬赏封妖任务')
                press_button('alt', 'v')
                guaji_cnt = 0
                guaji_status = False
                move_cnt =0
                while True:
                    time.sleep(1)
                    if detect_combat_or_not():
                        guaji_status = False
                        break
                    if not text_ocr.move_or_not():
                        guaji_cnt += 1
                        print(f'挂机{guaji_cnt}')
                    if guaji_cnt >= 20:
                        Daily_chumo.leave_team()
                        guaji_status = True
                        print('重新匹配')
                        break
                    if text_ocr.move_or_not():
                        move_cnt += 1
                        if move_cnt >= 3:
                            guaji_status = False
                            break
                if guaji_status:
                    continue
                elif not guaji_status:
                    break

        times = 0
        combat_status = True
        while True:
            time.sleep(5)
            if detect_combat_or_not() and combat_status == True:
                press_button('ctrl', 'a')
                times += 1
                print(f'第{times}次封妖')
                combat_status = False
                if times >= 5:
                    print('完成封妖')
                    stop_event.is_set()
                    break
            if detect_combat_or_not() == False:
                combat_status = True
            if detect_combat_or_not():
                combat_status = False
        while True:
            time.sleep(5)
            if not detect_combat_or_not():
                Daily_chumo.leave_team()
                press_button('F1', None)
