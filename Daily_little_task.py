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



class Daily_LittleTask:
    @staticmethod
    def juan_zhuang_bei():
        time.sleep(1.5)
        press_button('alt','o')
        time.sleep(1)
        text_ocr.ocr_target(region=(71,120,661,577),text='装备相关',click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(71, 120, 661, 577), text='7级装备',click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(71, 120, 661, 577), text='7级短棒之灵',click_or_not=True)
        for _ in range(8):
            locate_pos_click3('goumai',region=(317,556,534,183))
            time.sleep(1)
        Daily_shimen.press_esc()
        press_button('alt','e')
        time.sleep(1)
        if text_ocr.detect_pic('7jiling',region=(107,146,648,546)):
            locate_pos_click3('7jiling',region=(107,146,648,546),right_button=True)
        else:
            locate_pos_click3('beibao1', region=(107, 146, 648, 546))
            time.sleep(1)
            locate_pos_click3('7jiling', region=(107, 146, 648, 546), right_button=True)
        time.sleep(1)
        human_like_move(100+random.uniform(-10,10),536+random.uniform(-10,10))
        if not text_ocr.detect_pic('dagou',region=(575,474,320,238)):
            text_ocr.ocr_target(region=(575,474,320,238),text='不进行',click_or_not=True)
        for _ in range(8):
            text_ocr.ocr_target(region=(372,452,422,256), text='确定制造',click_or_not=True)
            time.sleep(0.3)
        Daily_shimen.press_esc()
        press_button('alt','w')
        time.sleep(1)
        text_ocr.ocr_target(region=(318,460,523,252), text='声望',click_or_not=True)
        time.sleep(1)
        text_ocr.ocr_target(region=(296,254,421,360), text='查看信息',click_or_not=True)
        time.sleep(1)
        locate_pos_click3('juanxian',region=(335,490,383,187))
        time.sleep(1)
        text_ocr.ocr_target(region=(317, 509, 421, 220), text='快速选择',click_or_not=True)
        time.sleep(1.2)
        for _ in range(2):
            text_ocr.ocr_target(region=(317, 509, 421, 220), text='确定',click_or_not=True)
        time.sleep(1.2)
        text_ocr.ocr_target(region=(259,299,432,234), text='确认', click_or_not=True)
        time.sleep(1.2)
        Daily_shimen.press_esc()
        print('捐献装备完成')


    @staticmethod
    def hualongding():
        press_button('alt','e')
        time.sleep(1)
        locate_pos_click3('hualongding',region=(124,117,512,366))
        time.sleep(1)
        text_ocr.ocr_target(region=(357,139,351,238),text='修炼',click_or_not=True)
        time.sleep(1)
        while not text_ocr.ocr_target_text(region=(314,256,385,150),text='额外修炼'):
            locate_pos_click3('zhengchangxiulian',region=(287,235,486,235))
            time.sleep(0.1)
        time.sleep(1)
        Daily_shimen.press_esc()
        time.sleep(1)
        press_button('alt', 'e')
        time.sleep(1)
        locate_pos_click3('hualongding', region=(124, 117, 512, 366))
        time.sleep(1)
        pos = text_ocr.detect_pic('longmaikongjian',region=(527,539,235,133))
        human_like_move(pos.x+231+random.uniform(1,5),pos.y+random.uniform(1,3))
        time.sleep(1)#173,150,520,548
        pyautogui.click()
        time.sleep(1)
        tuichu_goumai=False
        tuichu_times = 0
        while True:
            time.sleep(1.2)
            text_ocr.ocr_target(region=(173, 150, 520, 548), text='三色龙纹包', click_or_not=True)
            time.sleep(1)
            human_like_move(100 + random.randint(1, 10), 536 + random.randint(1, 10))
            time.sleep(1)
            while text_ocr.detect_pic('goumai', region=(173,150,520,548)):
                for _ in range(2):
                    locate_pos_click3('goumai', region=(173,150,520,548))
                    print('购买三色龙纹包')
                    time.sleep(1)
                if text_ocr.detect_pic('duihuan', region=(173,150,520,548)):
                    for _ in range(2):
                        locate_pos_click3('duihuan', region=(173,150,520,548))
                        time.sleep(1)
                    if text_ocr.ocr_target_text(region=(406,274,241,251),text='花费金币'):
                        print('没钱了，退出购买')
                        tuichu_goumai=True
                        time.sleep(1)
                        Daily_shimen.press_esc()
                        break
                    if text_ocr.detect_pic('queren', region=(173,150,520,548)):
                        locate_pos_click3('queren', region=(173,150,520,548))
                        time.sleep(1)
                        print('龙魂不足，银币兑换龙魂')
                    pos_x,pos_y =text_ocr.detect_pic('duihuan', region=(173,150,520,548))
                    human_like_move(pos_x+random.uniform(-100,-50),pos_y)
                    time.sleep(1)
                    pyautogui.click(button='right')
            if text_ocr.longhun_times():
                    locate_pos_click3('mianfeishuaxin',region=(448,148,200,200),confidence=0.8)
                    time.sleep(3)
                    locate_pos_click3('quedingshuaxin',region=(173,150,520,548),confidence=0.8)
                    time.sleep(3)
            if not text_ocr.longhun_times():
                tuichu_times+=1
            if tuichu_times >2:
                break
            if tuichu_goumai:
                Daily_shimen.press_esc()
                break
        print('结束龙魂购买')
        Daily_shimen.press_esc()







if __name__ == '__main__':
    move_window('高山流水')
    Daily_LittleTask.hualongding()