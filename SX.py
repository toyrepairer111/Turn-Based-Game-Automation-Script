import sys
import threading
import pyautogui
import asyncio
from text_ocr_file import text_ocr
from main import press_button,  move_window, time, human_like_move, detect_combat, locate_pos_click3,detect_combat_no_async
from chumo import Daily_chumo
from datetime import datetime




class Daily_sx:
    @staticmethod
    def sx():
        current_hour = datetime.now().hour
        print("当前系统时间:", current_hour)
        if 18<=current_hour<23:
            print('时间符合日常SX+TG')
        else:
            print('时间错误')
            sys.exit(0)
        while True:
            press_button('alt', 'y');time.sleep(2)
            todo_times = text_ocr.surplus_times('SX')
            print(f'生肖任务还剩{todo_times}次'), time.sleep(0.1)
            press_button('alt', 'y')
            if todo_times == 0:
                print('生肖任务已经完成，无法继续')
                break
            press_button('alt', 'v')
            time.sleep(2)
            text_ocr.ocr_target(region=(204, 180, 353-204,539-180), text='生肖', click_or_not=True)
            time.sleep(2)
            text_ocr.ocr_target(region=(596, 562, 239,106), text='开始匹配', click_or_not=True)
            while True:
                pi_pei_zhong = text_ocr.ocr_target(region=(201, 538, 360 - 201, 630 - 538), text=None, click_or_not=False)
                time.sleep(3)
                print('匹配队友中，请等待')
                print(pi_pei_zhong)
                time.sleep(1)
                if text_ocr.ocr_target(region=(596, 562, 239, 106), text='开始匹配', click_or_not=True):
                    print('重新开始匹配')
                if any('匹配' in item for item in pi_pei_zhong):
                    print('匹配队友中，请等待')
                    print(pi_pei_zhong)
                    time.sleep(10)
                else:
                    press_button('alt', 'v')
                    print('匹配成功')
                    break
            cnt = 1
            while True:
                detect_combat_no_async()
                time.sleep(1)
                cnt += 1
                print(f'已挂机{cnt}秒')
                if cnt > 20:
                        Daily_chumo.leave_team()
                        break


if __name__ == '__main__':
    pass