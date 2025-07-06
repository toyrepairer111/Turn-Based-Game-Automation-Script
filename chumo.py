import logging
import os
import random

import pyautogui
import asyncio

from Thread_function import detect_combat_chumo, auto_guozi
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, wen_jian, \
    detect_combat_no_async, detect_combat_or_not
import threading
from threading import Event


class Daily_chumo:
    @staticmethod
    def chumo():
        stop_event = Event()
        t1 = threading.Thread(target=Daily_chumo.auto_incense, args=(stop_event,))
        t1.start()
        t2 = threading.Thread(target=detect_combat_chumo, args=(stop_event,))
        t2.start()
        t3 = threading.Thread(target=auto_guozi, args=(stop_event,))
        t3.start()
        if not text_ocr.ocr_target_text((751, 144, 986 - 751, 625 - 144), text='除魔'):
            press_button('alt','y')
            todo_times = text_ocr.surplus_times('chumo');time.sleep(1)
            press_button('alt', 'y'), time.sleep(0.1)
            print(f'除魔任务还剩{todo_times}次'),time.sleep(0.1)
            if todo_times == 0:
                stop_event.set()
                print('除魔任务已经完成，无法继续')
                return
            map_name = text_ocr.ocr_target(region=(58, 27, 111, 26), text=None, click_or_not=False)
            if any('长安城' not in item for item in map_name):
                press_button('F7',None)
                text_ocr.ocr_target(region=(155, 137 ,561-155,196-137), text='长安城', click_or_not=True)
                human_like_move(354,342)
                pyautogui.click(354+random.uniform(-2,2),342+random.uniform(-2,2))
            time.sleep(1)
            press_button('alt', 'v')
            time.sleep(1)
            locate_pos_click3('pipei',region=(752,195,190,359))
            time.sleep(1)
            text_ocr.ocr_target(region=(599,590,825-599,654-590),text='创建队伍',click_or_not=True)
            time.sleep(1)
            text_ocr.ocr_target(region=(631,256, 809 - 631, 507 - 256), text='需要', click_or_not=True)
            time.sleep(1)
            text_ocr.ocr_target(region=(631, 256, 809 - 631, 507 - 256), text='愿意', click_or_not=True)
            time.sleep(1)
            text_ocr.ocr_target(region=(606, 357, 811-606, 510-357,), text='开始匹配', click_or_not=True)
            while True:
                ren_shu = text_ocr.ocr_target(region=(211,504,386-211,570-504), text=None, click_or_not=False)
                kaishi_ =text_ocr.ocr_target(region=(606, 357, 811-606, 510-357,), text=None, click_or_not=False)
                time.sleep(1)
                if any('级' in item for item in ren_shu ):
                    print('匹配成功，开始除魔任务')
                    time.sleep(1)
                    press_button('alt', 'v')
                    break
                if any('开始匹配'in item for item in kaishi_):
                    print('重新匹配')
                    if text_ocr.ocr_target(region=(606, 357, 811 - 606, 510 - 357,), text='开始匹配', click_or_not=True):
                        time.sleep(2)
            time.sleep(1)
            press_button('alt', 'y'),time.sleep(1.5)
            for _ in range(2):
                locate_pos_click3('chumo'),time.sleep(0.1)
            while True:
                time.sleep(1)
                if text_ocr.ocr_target(region=(351, 400, 577-364,557-400), text='我帮你', click_or_not=True):
                    text_ocr.ocr_target(region=(351, 400, 577 - 364, 557 - 400), text='没问题', click_or_not=True)
                    press_button('alt', 'y')
                    break
        tui_chu_duiwu_or_not = False
        chumo_nextround = False
        cnt = 1
        while True:
            time.sleep(1.2)
            cnt += 1
            chumo_times = text_ocr.rounde_number('除魔')
            if chumo_times != 0 and cnt % 90 == 0:
                print(f'这是除魔的第{chumo_times}环')
            if tui_chu_duiwu_or_not:
                Daily_chumo.leave_team()
                break
            if cnt % 120 == 0:
                if todo_times<=3:
                    continue
                else:
                    print('定期检查有没有狗跳队！')
                    press_button('alt', 'v');time.sleep(2)
                    ren_shu = text_ocr.ocr_target(region=(211, 504, 386 - 211, 570 - 504), text=None, click_or_not=False)
                    if any('级' in item for item in ren_shu):
                        print('队伍满员，无需匹配')
                        press_button('alt', 'v')
                    else:
                        from shimen import Daily_shimen
                        print('有狗跳队，需要匹配队员')
                        while True:
                            if detect_combat_or_not() is False:
                                for _ in range(2):
                                    time.sleep(0.5)
                                    Daily_shimen.press_esc()
                                    pyautogui.click(x=551 + random.uniform(-20, 20), y=448 + random.uniform(-20, 35),
                                                    button='Left')
                                break
                        press_button('alt', 'v')
                        time.sleep(1.2)
                        text_ocr.ocr_target(region=(442, 222, 382, 415), text='匹配队员', click_or_not=True)
                        print('匹配队友')
                        time.sleep(1.2)
                        text_ocr.ocr_target(region=(442,222,382,415),text='开始匹配', click_or_not=True)
                        print('开始匹配')
                        press_button('alt', 'v')
                        time.sleep(1.2)
                        for _ in range(5):
                            time.sleep(3)
                            text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='除魔', click_or_not=True)
            if chumo_times >=9:
                press_button('alt', 'y'), time.sleep(2)
                todo_times = text_ocr.surplus_times('chumo')
                press_button('alt', 'y')
                print(f'除魔任务还剩{todo_times}次'), time.sleep(0.1)
                if todo_times > 9:
                    chumo_nextround = True
                    cnt_text_times = 0
                    while True:
                        time.sleep(5)
                        if cnt_text_times % 30 == 0 :
                            print('准备继续接除魔任务')
                        cnt_text_times += 1
                        if text_ocr.ocr_target(region=(259,232, 643-259,608-232), text='继续', click_or_not=True):
                            for _ in range(5):
                                time.sleep(1)
                                text_ocr.ocr_target(region=(259, 232, 643 - 259, 608 - 232), text='继续',
                                                click_or_not=True)
                            break
                    while True:
                        time.sleep(2)
                        if text_ocr.ocr_target(region=(351, 400, 577-364,557-400), text='我帮你', click_or_not=True):
                            for _ in range(5):
                                time.sleep(1)
                                text_ocr.ocr_target(region=(351, 400, 577 - 364, 557 - 400), text='我帮你',
                                                    click_or_not=True)
                            break
                    if chumo_nextround:
                        print('除魔任务还有一轮结束')
                        while True:
                            time.sleep(10)
                            moving_status = Daily_chumo.moving()
                            if not detect_combat_or_not() and moving_status == True:
                                time.sleep(10)
                                if not detect_combat_or_not() and moving_status == True:
                                    print('检测是否完成除魔')
                                    press_button('alt', 'y'), time.sleep(1)
                                    todo_times2 = text_ocr.surplus_times('chumo2')
                                    press_button('alt', 'y')
                                    time.sleep(1.5)
                                    if todo_times2 == 0:
                                        stop_event.set()
                                        t2.join()
                                        print('捉鬼完成')
                                        time.sleep(5)
                                        Daily_chumo.press_esc()
                                        time.sleep(1)
                                        tui_chu_duiwu_or_not = True
                                        break

    @classmethod
    def press_esc(cls):
        time.sleep(1.2)
        pyautogui.press('esc')
        if text_ocr.ocr_target_text(region=(276, 478, 478, 187), text='游戏'):
            time.sleep(1.2)
            pyautogui.press('esc')

    @classmethod
    def moving(cls):
        while True:
            RGB1 = text_ocr.moving_detect(region=(51, 48, 52, 42))
            RGB3 = text_ocr.moving_detect(region=(651, 103, 52, 42))
            time.sleep(1.2)
            RGB2 = text_ocr.moving_detect(region=(51, 48, 52, 42))
            RGG4 = text_ocr.moving_detect(region=(651, 103, 52, 42))
            if RGB1 == RGB2 or RGB3 == RGG4:
                return True
            else:
                return False


    @staticmethod
    def auto_f9(stop_event=None):
        while True:
            try:
                if detect_combat_or_not() is False:
                    time.sleep(1+random.uniform(1, 3))
                    pyautogui.press('f9')
                    time.sleep(60+random.uniform(1, 3))
                elif stop_event and stop_event.is_set():
                    break
            except Exception as e:
                print(f'{e}')
                break

    @staticmethod
    def auto_incense(stop_event):
        while not stop_event.is_set():
            try:
                if text_ocr.detect_pic('xiang',region=(900,93,1028-900,148-93)):
                    print('已使用香')
                    time.sleep(3588)
                else:
                    time.sleep(2)
                    if text_ocr.ocr_target(region=(878,650,996-878,756-650), text='使用', click_or_not=True):
                        time.sleep(3588)
            except Exception as e:
                pass

    @staticmethod
    def leave_team():
        press_button('alt', 'v')
        time.sleep(2)
        if text_ocr.ocr_target_text(region=(438, 480, 400,220), text='退出'):
            while True:
                if text_ocr.ocr_target(region=(438, 480, 400,220), text='退出',click_or_not=True):
                    time.sleep(1)
                    text_ocr.ocr_target(region=(438, 480, 400, 220), text='退出', click_or_not=True)
                    print('正在退队')
                    break
            for _ in range(5):
                if text_ocr.ocr_target(region=(438, 480, 400,220), text='创建',click_or_not=True):
                    press_button('alt', 'v')

        else:
            print('无需退队')
            press_button('alt', 'v')



ppocr_logger = logging.getLogger("ppocr")
ppocr_logger.setLevel(logging.ERROR)  # 只显示 ERROR 以上级别
# 关闭所有第三方库的 DEBUG 日志
logging.getLogger().setLevel(logging. ERROR)





if __name__ == "__main__":
    move_window('风驰电掣')
    Daily_chumo.leave_team()
