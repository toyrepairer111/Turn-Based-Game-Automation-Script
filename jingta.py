import logging
import random
import threading
from datetime import datetime

import pyautogui
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, bb_dead, detect_combat_or_not, move_window2
from chumo import Daily_chumo
from threading import Event
from shimen import Daily_shimen

class Jingta:
    @staticmethod
    def jingta(area):
        while True:
            current_hour = datetime.now().hour
            if current_hour >= 21:
                break
            else:
                print('等待十分钟')
                time.sleep(600)
        Daily_chumo.leave_team()
        t3 = threading.Thread(target=Daily_chumo.auto_f9, daemon=True)
        t3.start()
        click_time =True
        cnt = 0
        cnt2 =0
        cnt3 = 0
        Daily_shimen.press_esc()
        if not (text_ocr.ocr_target_text(region=(751, 144, 986 - 751, 625 - 144), text='镜中塔') or detect_combat_or_not()) :
            press_button('alt','v')
            time.sleep(1)
            text_ocr.ocr_target(region=(599, 590, 825 - 599, 654 - 590), text='创建队伍', click_or_not=True)
            time.sleep(1)
            text_ocr.ocr_target(region=(181,169,174,467), text='全部队伍', click_or_not=True)
            time.sleep(1)
            text_ocr.ocr_target(region=(436,214,377,365), text='镜塔', click_or_not=True)
            time.sleep(1)
            text_ocr.ocr_target(region=(606, 357, 811-606, 510-357,), text='开始匹配', click_or_not=True)
            time.sleep(1)
            text_ocr.ocr_target(region=(306,277, 451,302), text='开始匹配', click_or_not=True)
            while True:
                time.sleep(1)
                ren_shu = text_ocr.ocr_target(region=(211,504,386-211,570-504), text=None, click_or_not=False)
                if any('级' in item for item in ren_shu ):
                    print('匹配成功，开始镜塔任务')
                    time.sleep(1)
                    press_button('alt', 'v')
                    break
            press_button('alt', 'y'), time.sleep(1.5)
            for _ in range(2):
                text_ocr.ocr_target(region=(179,444,706,236),text='镜塔', click_or_not=True)
            Daily_shimen.moving()
            while True:
                if text_ocr.ocr_target(region=(351, 400, 577-364,557-400), text='我要参加', click_or_not=True):
                    press_button('alt', 'y')
                    break
                time.sleep(1)
        time.sleep(6)
        while True:
            in_combat = detect_combat_or_not()
            if in_combat is False:
                time.sleep(1)
                if cnt2%10 == 0:
                    print(f"是否需要点击任务导航:{click_time}")
                cnt2 += 1
                if text_ocr.detect_pic('baoxiang'):
                    random_treasure = random.randint(1,3)
                    match random_treasure:
                        case (1):
                            locate_pos_click3('baoxiang',region=(303,347,134,150))
                        case (2):
                            locate_pos_click3('baoxiang',region=(445,350,134,150))
                        case (3):
                            locate_pos_click3('baoxiang',region=(581,349,134,150))
                    time.sleep(3.5)
                    Daily_shimen.press_esc()
                    click_time = True
                    cnt = 0
                if click_time :
                    while True:
                        if text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='镜中塔', click_or_not=True):
                            time.sleep(0.5)
                            text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='镜中塔',
                                                click_or_not=True)
                            print('导航镜塔')
                            break
                        if text_ocr.move_or_not() == False and detect_combat_or_not() == False:
                            break
                    print('导航镜塔2')
                    click_time = False
                    cnt = 0
                if text_ocr.ocr_target(region=(351, 400, 448,129), text='简单难度', click_or_not=True):
                    time.sleep(2.5)
                    text_ocr.ocr_target(region=(351, 400, 448, 129), text='确定', click_or_not=True)
                    print(f'开始')
                    cnt = 0
            if text_ocr.move_or_not() == False and detect_combat_or_not() == False:
                cnt += 1
                time.sleep(1)
                print(f'已挂机：{cnt}')
                if cnt >20:
                    if not text_ocr.ocr_target_text(region=(751, 144, 986 - 751, 625 - 144), text='镜中塔'):
                        print('镜塔结束，退出')
                        Daily_shimen.press_esc()
                        time.sleep(0.5)
                        Daily_chumo.leave_team()
                        break
            else:
                if in_combat:
                    if cnt3%12==0:
                        print('战斗中')
                        press_button('ctrl', 'a')
                    time.sleep(10)
                    cnt3+=1
                    click_time = True
                else:
                    Daily_shimen.moving()
                    time.sleep(0.5)
                    click_time = False

if __name__ == '__main__':
    move_window('风华绝代')
    Jingta.jingta()




