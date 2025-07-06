import logging
import os
import random
import re
import threading
import pyautogui
from paddle.distributed.fleet.fleet_executor_utils import origin

from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, bb_dead, detect_combat_or_not, detect_picture2
from chumo import Daily_chumo
from shimen import Daily_shimen
from qianzhicaozuo import use_xiang


class Daily_xiulian:

    patterns = {
        r'寻物': 'function_collect',
        r'找人': 'function_find_people',
        r'疯道人': 'function_find_bitch',
    }
    @classmethod
    def xiulian(cls):
        try:
            use_xiang()
            time.sleep(1)
            press_button('alt', 'y')
            time.sleep(1.2)
            todo_times = text_ocr.surplus_times('xiulian')
            press_button('alt', 'y')
            stuck_count = 0
            if todo_times==0:
                print('修炼已完成')
                return
            while todo_times>0:
                if todo_times %2 == 0:
                    press_button('alt', 'y')
                    time.sleep(1.2)
                    todo_times = text_ocr.surplus_times('xiulian')
                    press_button('alt', 'y')
                print(f'修炼还有{todo_times}环')
                task_text_list = text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text=None, click_or_not=False)
                task_text = ' '.join(task_text_list)
                pattern_finish = r'.*?(修炼)'
                if re.search(pattern_finish, task_text) is None and todo_times <= 0:
                    print('修炼已经完成，退出')
                    return
                if stuck_count >=3:
                    print('识别不到修炼任务，退出')
                    break
                if re.search(pattern_finish, task_text) is None:
                    print(f'一开始识别到的{task_text}')
                    print('领取修炼任务')
                    press_button('alt', 'y')
                    time.sleep(1.2)
                    locate_pos_click3('xiulian')
                    press_button('alt', 'y')
                    Daily_shimen.moving()
                    time.sleep(1.2)
                    text_ocr.ocr_target(region=(359, 394, 360, 142), text='领取修炼任务', click_or_not=True)
                    time.sleep(1.2)
                    Daily_shimen.press_esc()
                    time.sleep(1.2)
                found = False
                for pattern, function in cls.patterns.items():
                    task_text_list = text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text=None,
                                                         click_or_not=False)
                    task_text = ' '.join(task_text_list)
                    core_match = re.search(r'【修炼任务】.+', task_text)
                    if core_match :
                        task_text = core_match.group()
                    if match:= re.search(pattern,task_text):
                        print(f"匹配成功 - 模式: {pattern} → 函数: {function}")
                        Daily_shimen.press_esc()
                        time.sleep(1.2)
                        getattr(cls,function)()
                        found = True
                        todo_times -= 1
                        stuck_count = 0
                        break
                if not found:
                    print('检测出错，识别不到修炼任务')
                    stuck_count += 1
                else:
                    stuck_count = 0
        except Exception as e:
            pass

    @classmethod
    def function_collect(cls):
        try:
            pattern = r'.*?修炼任务.*?寻物.*?(完成)'
            task_text_list = text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text=None, click_or_not=False)
            task_text = ' '.join(task_text_list).replace(' ', '')
            while re.search(pattern, task_text) is None:
                press_button('alt', 'j')
                time.sleep(1)
                for _ in range(3):
                    time.sleep(0.5)
                    locate_pos_click3('goumai', region=(317, 556, 534, 183))
                press_button('alt', 'j')
                task_text_list = text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text=None, click_or_not=False)
                task_text = ' '.join(task_text_list).replace(' ', '')
            text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='修炼任务', click_or_not=True)
            human_like_move(502+random.uniform(-50,50),412+random.uniform(-50,50))
            Daily_shimen.moving()
            if text_ocr.ocr_target(region=(359, 394, 360, 142), text='交任务', click_or_not=True):
                time.sleep(2)
                text_ocr.ocr_target(region=(359, 394, 360, 142), text='寻物', click_or_not=True)
                time.sleep(2)
                cls.give_article()
                time.sleep(2)
                print('全部点击完成')
                text_ocr.ocr_target(region=(283, 499, 214, 156), text='确定', click_or_not=True)
                time.sleep(1.2)
                Daily_shimen.press_esc()
            else:
                if text_ocr.detect_pic('jiyuwupin'):
                    time.sleep(2)
                    cls.give_article()
                    time.sleep(2)
                    print('全部点击完成')
                    text_ocr.ocr_target(region=(283, 499, 214, 156), text='确定', click_or_not=True)
                    time.sleep(1.2)
                    Daily_shimen.press_esc()
        except Exception as e:
            pass




    @classmethod
    def function_find_people(cls):
        try:
            text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='修炼任务', click_or_not=True)
            human_like_move(502 + random.uniform(-50, 50), 412 + random.uniform(-50, 50))
            Daily_shimen.moving()
            time.sleep(3)
            if detect_combat_or_not():
                while True:
                    time.sleep(20)
                    if detect_combat_or_not() == False:
                        time.sleep(1.2)
                        Daily_shimen.press_esc()
                        break

        except Exception as e:
            pass

    @classmethod
    def function_find_bitch(cls):
        try:
            text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='修炼任务', click_or_not=True)
            human_like_move(502 + random.uniform(-50, 50), 412 + random.uniform(-50, 50))
            Daily_shimen.moving()
            time.sleep(3)
            while True:
                time.sleep(1)
                if detect_combat_or_not() :
                    print('打疯道人')
                    time.sleep(1.2)
                    press_button('ctrl', 'a')
                    break
            while True:
                time.sleep(1)
                if detect_combat_or_not() == False:
                    print('结束与疯道人战斗')
                    time.sleep(2)
                    Daily_shimen.press_esc()
                    break

        except Exception as e:
            pass

    @classmethod
    def give_article(cls):
        try :
            if text_ocr.detect_pic('jiyuwupin'):
                pos = text_ocr.detect_pic('jiyuwupin')#572 ， 188  526 , 251   295 337  190 59
            else:
                text_ocr.ocr_target(region=(359, 394, 360, 142), text='寻物', click_or_not=True)
                time.sleep(1.2)
                pos = text_ocr.detect_pic('jiyuwupin')
            origin_x =pos.x
            origin_y =pos.y
            kongbeibao = False
            finish_timing = text_ocr.ocr_target(region=(origin_x-277, origin_y+149,190,59), text=None, click_or_not=False)
            page = 0
            for _ in range(5):
                time.sleep(0.2)
                if text_ocr.detect_pic(f'beibao{page}'):
                    print('点击行囊')
                    locate_pos_click3(f'beibao{page}', region=(625,101, 293,316))
                    break
            while not finish_timing  and kongbeibao is False:
                started_x = pos.x - 46
                started_y = pos.y + 63
                kongbeibao_y = started_y - 30
                for j in range(1,9):
                    for i in range(5):
                        target_x =started_x+i*50
                        if text_ocr.detect_pic('kongbeibao',region=(target_x-30, kongbeibao_y, 55,55))is not False:
                            print('已经到头啦结束点击啦')
                            kongbeibao = True
                            break
                        human_like_move(target_x+random.uniform(-3,3), started_y+random.uniform(-3,3))
                        pyautogui.click(target_x+random.uniform(-3,3), started_y+random.uniform(-3,3))
                        time.sleep(0.1)
                    started_y += 50
                    kongbeibao_y = started_y-30
                    if kongbeibao:
                        break
                finish_timing = text_ocr.ocr_target(region=(origin_x - 277, origin_y + 149, 190, 59), text=None,
                                                    click_or_not=False)
                page += 1
                if  locate_pos_click3(f'beibao{page}',region=(703, 204, 133, 247)) is not False:
                    print('page是{}'.format(page))
                    print('进入下一页')
                    time.sleep(1)
                else:
                    print('page是{}'.format(page))
                    print('没有背包可以点了，走咯')
                    break
        except Exception as e:
            pass



if __name__ == '__main__':
    pass