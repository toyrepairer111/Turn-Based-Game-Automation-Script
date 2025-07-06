import logging
import os
import random
import re
import threading
import pyautogui
from paddle.distributed.fleet.fleet_executor_utils import origin

import qianzhicaozuo
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, bb_dead, detect_combat_or_not, detect_picture2, move_window_3
from chumo import Daily_chumo
from shimen import Daily_shimen
from qianzhicaozuo import use_xiang

class fish:

    @staticmethod
    def fishing(times,gamearea):
        try:
            move_window_3(f'{gamearea}')
            time.sleep(3)
            failure_times = 0
            for each_times in range(times):
                qianzhicaozuo.use_xiang()
                time.sleep(1)
                for _ in range(5):
                    time.sleep(0.2)
                    if text_ocr.ocr_target(region=(362,519,316,159),text='关闭',click_or_not=True):
                        time.sleep(1)
                        print('收获一只小伙伴')
                        locate_pos_click3('huobantujian',region=(162,177,197,315),right_button=True)
                        time.sleep(0.2)
                        break
                if text_ocr.detect_pic('hook',region=(340,142,408,547)):
                    pyautogui.press('F1')
                    print('开始抛竿')
                time.sleep(random.uniform(2,4))
                pyautogui.press('F1')
                print('抛竿成功')
                while True:
                    time.sleep(random.uniform(0.8, 2))
                    if text_ocr.detect_pic('hook_back',region=(340,142,408,547)):
                        pyautogui.press('space')
                        pyautogui.press('space')
                        print('收杆成功')
                        break
                hook_times = 0
                while True:
                    if text_ocr.detect_pic('run_fish',region=(314,125,211,374)):
                        print('拉杆中，用力啊')
                        i = 2
                        max_ = 10
                        while text_ocr.detect_pic('run_fish',region=(294,103,463,308)):
                            pyautogui.keyDown('space')
                            hook_times += 1
                            if hook_times % i == 0:
                                pyautogui.keyUp('space')
                                if i <max_:
                                    i+=3
                                else:
                                    i = max_
                    if text_ocr.detect_pic('hook', region=(340, 142, 408, 547)):
                        failure_times += 1
                        print(f'获得未知鱼类{failure_times}个或者钓鱼失败')
                        time.sleep(random.uniform(0.1, 1.5))
                        break
                    if text_ocr.ocr_target(region=(338,515,366,106), text='收藏', click_or_not=True):
                        print('拉杆完毕，收藏鱼')
                        print(f'第{each_times+1}次钓鱼,其中失败了{failure_times}次')
                        time.sleep(random.uniform(0.1, 1.5))
                        human_like_move(636+random.uniform(-30,30),536+random.uniform(-30,30))
                        break
                    if text_ocr.ocr_target(region=(299, 331, 426, 314), text='快速出售', click_or_not=True):
                        print('收杆完美，直接得鱼')
                        time.sleep(0.1)
                        print(f'第{each_times+1}次钓鱼,其中失败了{failure_times}次')
                        human_like_move(636 + random.uniform(-30, 30), 536 + random.uniform(-30, 30))
                        time.sleep(random.uniform(0.1, 1.5))
                        break
            for i in range(1, 6):
                print(f'还有{6 - i}秒关机')
                time.sleep(1)
            os.system("shutdown /s /t 0")


        except Exception as e:
            print(e)

if __name__ == '__main__':
    move_window_3('高山流水')
    fish.fishing(41)