import os
import random
import sys
import threading
import pyautogui
import asyncio
import logging

from Daily_little_task import Daily_LittleTask
import Fish
from huodong1 import Menpai
from jingta import Jingta
from SX import Daily_sx
from TG import Daily_tg
from fengyao import Daily_fengyao
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, wen_jian, dig_treasure, async_guaji
from chumo import Daily_chumo
from datetime import datetime
from fuben import Daily_fuben
from shimen import Daily_shimen
from qianzhicaozuo import use_xiang
from xiulian import Daily_xiulian
from Fish import fish
from xuanshang import Xuanshang_chumo,Xuanshang_fengyao

ppocr_logger = logging.getLogger("ppocr")
ppocr_logger.setLevel(logging.ERROR)  # 只显示 ERROR 以上级别
# 关闭所有第三方库的 DEBUG 日志
logging.getLogger().setLevel(logging. ERROR)


def all_task(game_area):
    move_window(f'{game_area}')
    stop_event = threading.Event()
    t1 = threading.Thread(target=Daily_chumo.auto_f9, args=(stop_event,))
    t1.start()
    use_xiang()
    stop_event.set()
    time.sleep(0.7)
    Daily_shimen.shimen() # 需取消现金限制
    time.sleep(0.7)
    Daily_xiulian.xiulian()
    time.sleep(0.7)
    wen_jian()  # 需选定是问剑
    time.sleep(0.7)
    Daily_fuben.fuben()
    time.sleep(0.7)
    Daily_fengyao.fengyao()
    time.sleep(0.7)
    Daily_chumo.chumo()
    time.sleep(0.7)
    stop_event.set()





def all_task_turn_off_computer(game_area):
    move_window(f'{game_area}')
    stop_event = threading.Event()
    t1 = threading.Thread(target=Daily_chumo.auto_f9, args=(stop_event,))
    t1.start()
    use_xiang()
    time.sleep(0.7)
    Daily_shimen.shimen() # 需取消现金限制
    time.sleep(0.7)
    #Daily_xiulian.xiulian()
    time.sleep(0.7)
    wen_jian()  # 需选定是问剑
    time.sleep(0.7)
    Daily_fuben.fuben()
    time.sleep(0.7)
    Daily_chumo.chumo()
    time.sleep(0.7)
    Daily_fengyao.fengyao()
    stop_event.set()
    time.sleep(0.7)
    for i in range(1,6):
        print(f'还有{6-i}秒关机')
        time.sleep(1)
    os.system("shutdown /s /t 0")

def sx_tg(game_area):
    move_window(f'{game_area}')
    while True:
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        if current_hour >=19 or (current_hour == 18 and current_minute >= 30):
                Daily_chumo.leave_team()
                Daily_sx.sx()
                time.sleep(5)
                Daily_tg.tg()
                break
        else:
            print('等待十分钟')
            time.sleep(600)




def begin_daily_task(game_area):
    for times in range(1,5):
        status=all_task(f'{game_area}')
        if status == 1997:
            print('已完成一个账号，下一个，自动化拉满！')
        while True:
            time.sleep(1)
            pyautogui.press('esc')
            time.sleep(0.7)
            if text_ocr.ocr_target(region=(272,480,468,231),text='重新登录',click_or_not=True):
                 break
        time.sleep(0.7)
        while True:
             if text_ocr.ocr_target(region=(347,672,377,82),text='开始游戏',click_or_not=True):
                 break
        time.sleep(0.7)
        while True:
             if text_ocr.ocr_target(region=(430,624,185,61),text='开始游戏',click_or_not=True):
                 break
        time.sleep(2)
        if times == 1:
            human_like_move(927+random.uniform(-20,20),358+random.uniform(-20,20))
            time.sleep(0.7)
            pyautogui.click()
            while True:
                if text_ocr.ocr_target(region=(430, 624, 185, 61), text='开始游戏', click_or_not=True):
                    break
        elif times == 2:
            human_like_move(933 + random.uniform(-20,20), 437 + random.uniform(-20,20))
            time.sleep(0.7)
            pyautogui.click()
            while True:
                if text_ocr.ocr_target(region=(430, 624, 185, 61), text='开始游戏', click_or_not=True):
                    break
        elif times == 3:
            human_like_move(928 + random.uniform(-20,20), 518 + random.uniform(-20,20))
            time.sleep(0.7)
            pyautogui.click()
            while True:
                if text_ocr.ocr_target(region=(430, 624, 185, 61), text='开始游戏', click_or_not=True):
                    break
        time.sleep(5)
    for i in range(1,6):
        print('执行完毕咯，关机')
        print(f'还有{6-i}秒关机')
        time.sleep(1)
    os.system("shutdown /s /t 0")



def begin_daily_sx_tg(game_area):
    stop_event = threading.Event()
    t1 = threading.Thread(target=Daily_chumo.auto_f9, args=(stop_event,))
    t1.start()
    for times in range(1,5):
        status=sx_tg(f'{game_area}')
        if status == 1997:
            print('这个号完成SX和TG咯，继续搞下一个')
        if times == 4:
            print('最后一个号啦，干完了，爽！')
            break
        while True:
             pyautogui.press('esc')
             time.sleep(0.7)
             if text_ocr.ocr_target(region=(272,480,468,231),text='重新登录',click_or_not=True):
                 break
        time.sleep(0.7)
        while True:
             if text_ocr.ocr_target(region=(347,672,377,82),text='开始游戏',click_or_not=True):
                 break
        time.sleep(0.7)
        while True:
             if text_ocr.ocr_target(region=(430,624,185,61),text='开始游戏',click_or_not=True):
                 break
        time.sleep(2)
        if times == 1:
            human_like_move(927+random.uniform(-20,20),358+random.uniform(-20,20))
            time.sleep(0.7)
            pyautogui.click()
            while True:
                if text_ocr.ocr_target(region=(430, 624, 185, 61), text='开始游戏', click_or_not=True):
                    break
        elif times == 2:
            human_like_move(933 + random.uniform(-20,20), 437 + random.uniform(-20,20))
            time.sleep(0.7)
            pyautogui.click()
            while True:
                if text_ocr.ocr_target(region=(430, 624, 185, 61), text='开始游戏', click_or_not=True):
                    break
        elif times == 3:
            human_like_move(928 + random.uniform(-20,20), 518 + random.uniform(-20,20))
            time.sleep(0.7)
            pyautogui.click()
            while True:
                if text_ocr.ocr_target(region=(430, 624, 185, 61), text='开始游戏', click_or_not=True):
                    break
        time.sleep(5)
    stop_event.set()

def shut_down():
    for i in range(1,6):
        print('执行完毕咯，关机')
        print(f'还有{6-i}秒关机')
        time.sleep(1)
    os.system("shutdown /s /t 0")

def Daily_xijie():
    while True:
        current_hour = datetime.now().hour
        if current_hour >=22 :
            print('等待十分钟')
            time.sleep(600)
        else:
            break
    Daily_LittleTask.juan_zhuang_bei()
    Daily_LittleTask.hualongding()
    Daily_shimen.press_esc()

if __name__ == '__main__':
    game_area = '高山流水'
    move_window(f'{game_area}')
    Daily_xijie()
    #dig_treasure(f'{game_area}')
    all_task(f'{game_area}')
    #Menpai.menpai(10)
    #sx_tg(f'{game_area}')
    #Menpai.menpai(10)
    #Jingta.jingta(f'{game_area}')
    #all_task(f'{game_area}')
    #Xuanshang_fengyao.fengyao()
    #asyncio.run(async_guaji(f'{game_area}'))
    shut_down()

    












