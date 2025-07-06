import logging
import random
import threading

import pyautogui

from shimen import Daily_shimen
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, bb_dead, detect_combat_or_not
from chumo import Daily_chumo


class Daily_fuben:
    @staticmethod
    def fuben():
        map_name = text_ocr.ocr_target(region=(58, 27, 111, 26), text=None, click_or_not=False)
        if any('长安城' not in item for item in map_name):
            press_button('F7', None)
            text_ocr.ocr_target(region=(155, 137, 561 - 155, 196 - 137), text='长安城', click_or_not=True)
            human_like_move(354, 342)
            pyautogui.click(x=354 + random.uniform(-2, 2), y=342 + random.uniform(-2, 2))
        press_button('alt','w');time.sleep(1)
        level_info = text_ocr.level_info()
        print(f'等级是{level_info}级')
        press_button('alt', 'w')
        target_fuben = ''
        if level_info<90:
            target_fuben = 'fuben1'
        elif level_info<=119:
            target_fuben = 'fuben2'
        else:
            target_fuben = 'fuben3'
        while True:
            cnt = 0
            press_button('alt', 'y');
            time.sleep(2)
            todo_times = text_ocr.surplus_times(target_fuben)
            print(f'副本任务还剩{todo_times}次');
            time.sleep(0.1)
            press_button('alt', 'y');
            time.sleep(0.1)
            if todo_times == 0:
                print('副本任务已经完成，无法继续')
                break
            while True:
                press_button('alt', 'v')
                time.sleep(2)
                text_ocr.ocr_target(region=(204, 180, 353-204,539-180), text='副本', click_or_not=True)
                time.sleep(2)
                text_ocr.ocr_target(region=(596, 562, 239,106), text='开始匹配', click_or_not=True)
                time.sleep(2)
                text_ocr.ocr_target(region=(365,301,338,132), text='愿意成为队员', click_or_not=True)
                cnt2=1
                while True:
                    pi_pei_zhong = text_ocr.ocr_target(region=(214, 594, 184,36), text=None, click_or_not=False)
                    team_off = text_ocr.ocr_target(region=(356,583, 466,48), text=None, click_or_not=False)
                    map_name = text_ocr.ocr_target(region=(58,27, 111,26), text=None, click_or_not=False)
                    print(map_name)
                    print('匹配队友中，请等待')
                    print(pi_pei_zhong)
                    time.sleep(10)
                    cnt2 += 1
                    if any('正在匹配' in item for item in pi_pei_zhong):
                        print('匹配队友中，请等待')
                        print(pi_pei_zhong)
                    elif any('开始匹配' in item for item in team_off):
                        print('被T了，重新匹配')
                        print(team_off)
                        press_button('alt', 'v')
                        break
                    elif any('长安城' not in item for item in map_name):
                        print('匹配成功，已经进入副本')
                        press_button('alt', 'v')
                        break
                    elif detect_combat_or_not(): #90副本也会显示在长安
                        print('匹配成功，已经进入副本')
                        press_button('alt', 'v')
                        break
                    elif cnt2 >= 12:
                        print('队长挂机，重新匹配，退队')
                        Daily_chumo.leave_team()
                        time.sleep(1)
                        break
                if any('长安城' not in item for item in map_name):
                    break
            cnt2 = 1
            while True:
                print('副本挂机中')
                detect_combat_no_async()
                map_name = text_ocr.ocr_target(region=(55, 31, 144, 24), text=None, click_or_not=False)
                if any('长安城'  in item for item in map_name):
                    print('副本已经完成一次')
                    time.sleep(1)
                    pyautogui.press('esc')
                    break
                time.sleep(30)
                cnt += 1
                if cnt % 4 == 0:
                    Daily_shimen.press_esc()
                    print('定期检查有没有狗跳队！')
                    press_button('alt', 'v')
                    time.sleep(2)
                    ren_shu = text_ocr.ocr_target(region=(211, 504, 386 - 211, 570 - 504), text=None,
                                                  click_or_not=False)
                    if any('级' in item for item in ren_shu):
                        print('队伍满员，无需退出队伍')
                        press_button('alt', 'v')
                    else:
                        press_button('alt', 'v')
                        time.sleep(2)
                        Daily_chumo.leave_team()
                        print('返回长安城重新匹配')
                        break
            while True:
                cnt += 1
                time.sleep(1)
                map_name = text_ocr.ocr_target(region=(55, 31, 144, 24), text=None, click_or_not=False)
                if cnt > 120:
                    if any('长安城' in item for item in map_name):
                        print('挂机时长过久，重新匹配副本')
                        time.sleep(1)
                        Daily_shimen.press_esc()
                        Daily_chumo.leave_team()
                        break
                    else:
                        time.sleep(1)
                        Daily_shimen.press_esc()
                        print('继续副本')
                        break

ppocr_logger = logging.getLogger("ppocr")
ppocr_logger.setLevel(logging.ERROR)  # 只显示 ERROR 以上级别
# 关闭所有第三方库的 DEBUG 日志
logging.getLogger().setLevel(logging. ERROR)

if __name__ == '__main__':
    Daily_fuben.fuben()





