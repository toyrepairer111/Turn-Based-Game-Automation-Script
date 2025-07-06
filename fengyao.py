import random
import threading
import pyautogui
import asyncio

from Thread_function import auto_guozi
from text_ocr_file import text_ocr
from main import press_button,  move_window, time, human_like_move, detect_combat, locate_pos_click3,detect_combat_no_async
from chumo import Daily_chumo


class Daily_fengyao:
    @staticmethod
    def fengyao():
        stop_event = threading.Event()
        t3 = threading.Thread(target=auto_guozi, args=(stop_event,))
        t3.start()
        while True:
            press_button('alt', 'y');time.sleep(2)
            todo_times = text_ocr.surplus_times('fengyao')
            print(f'封妖任务还剩{todo_times}次');time.sleep(0.1)
            press_button('alt', 'y');time.sleep(0.1)
            if todo_times == 0 :
                print('封妖任务已经完成，无法继续')
                stop_event.set()
                return 1997
            press_button('alt', 'v')
            time.sleep(2)
            text_ocr.ocr_target(region=(204, 180, 353-204,539-180), text='降妖', click_or_not=True)
            time.sleep(2)
            text_ocr.ocr_target(region=(596, 562, 239,106), text='开始匹配', click_or_not=True)
            while True:
                pi_pei_zhong = text_ocr.ocr_target(region=(201, 538, 360 - 201, 630 - 538), text=None, click_or_not=False)
                time.sleep(3)
                print('匹配队友中，请等待')
                print(pi_pei_zhong)
                time.sleep(10)
                if any('匹配' in item for item in pi_pei_zhong):
                    print('匹配队友中，请等待')
                    print(pi_pei_zhong)
                    time.sleep(1)
                else:
                    print('匹配成功，开始降妖任务')
                    press_button('alt', 'v')
                    break

            cnt = 1
            while True:
                detect_combat_no_async()
                time.sleep(1)
                cnt += 1
                print(f'已挂机{cnt}秒')
                if cnt > 120: #挂机2分钟，查看是否已经完成封妖
                    press_button('alt', 'y');time.sleep(2)
                    todo_times = text_ocr.surplus_times('fengyao')
                    todo_times2 = text_ocr.surplus_times('fengyao2')
                    print(f'封妖任务还剩{todo_times}次'), time.sleep(0.1)
                    press_button('alt', 'y')
                    if todo_times == 0 or todo_times2 == 0:
                        print('封妖任务已经完成,返回主城中')
                        time.sleep(1)
                        pyautogui.press('esc')
                        Daily_chumo.leave_team()
                        map_name = text_ocr.ocr_target(region=(58, 27, 111, 26), text=None, click_or_not=False)
                        if any('长安城' not in item for item in map_name):
                            press_button('F7', None)
                            text_ocr.ocr_target(region=(155, 137, 561 - 155, 196 - 137), text='长安城',
                                                click_or_not=True)
                            human_like_move(354, 342)
                            pyautogui.click(x=354+random.uniform(-2,2),y=342+random.uniform(-2,2))
                        break
                    elif todo_times != 0 :
                        print('封妖任务未完成，队长挂机，返回主城重新匹配')
                        time.sleep(1)
                        pyautogui.press('esc')
                        Daily_chumo.leave_team()
                        map_name = text_ocr.ocr_target(region=(58, 27, 111, 26), text=None, click_or_not=False)
                        if any('长安城' not in item for item in map_name):
                            press_button('F7', None)
                            text_ocr.ocr_target(region=(155, 137, 561 - 155, 196 - 137), text='长安城',
                                                click_or_not=True)
                            human_like_move(354, 342)
                            pyautogui.click(x=354+random.uniform(-2,2),y=342+random.uniform(-2,2))
                        break

if __name__ == '__main__':
    pass


