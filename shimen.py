import logging
import os
import random
import re
import threading
import pyautogui
from text_ocr_file import text_ocr
from main import press_button, move_window, time, human_like_move, detect_combat, locate_pos_click3, \
    detect_combat_no_async, bb_dead, detect_combat_or_not, detect_picture2
from chumo import Daily_chumo


class Daily_shimen:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(script_dir, 'renwu123')
    article_to_pic = {'叫花鸡':os.path.join(image_dir, "jiaohuaji.png"),
                      '女儿红': os.path.join(image_dir, "nverhong.png"),
                      '珍露酒': os.path.join(image_dir, "zhenlujiu.png"),
                      '醉生梦死': os.path.join(image_dir, "zuishengmengsi.png"),
                      '玉蓉糕': os.path.join(image_dir, "yuronggao.png"),
                      '珍珠丸子': os.path.join(image_dir, "zhenzhuwanzi.png"),
                      '百味酒': os.path.join(image_dir, "baiweijiu.png"),
                      '蛇胆酒': os.path.join(image_dir, "shedanjiu.png"),
                      '长寿面': os.path.join(image_dir, "changshoumian.png"),
                      '脆皮乳猪': os.path.join(image_dir, "cuipiruzhu.png"),
                      '佛跳墙': os.path.join(image_dir, "fotiaoqiang.png"),
                      '香辣蟹': os.path.join(image_dir, "xianglaxia.png"),
                      '玉琼浆': os.path.join(image_dir, "yuqiongjiang.png"),
                      '五味羹': os.path.join(image_dir, "wuweigeng.png"),
                      '八宝粥': os.path.join(image_dir, "babaozhou.png"),
                      '踏雪燕窝': os.path.join(image_dir, "taxueyanwo.png"),
                      '血还丹': os.path.join(image_dir, "xuehuandan.png"),
                      '聚元丹': os.path.join(image_dir, "juyuandan.png"),
                      '济生丸': os.path.join(image_dir, "jishengwan.png"),
                      '玉蟾丸': os.path.join(image_dir, "yuchanwan.png"),
                      '还灵散': os.path.join(image_dir, "huanlingsan.png"),
                      '九转还魂丹': os.path.join(image_dir, "jiuzhuanhuanhundan.png"),
                      '归魂露': os.path.join(image_dir, "guihunlu.png"),
                      '灵心丸': os.path.join(image_dir, "lingxinwan.png"),
                      '驱魔丹': os.path.join(image_dir, "qumodan.png"),
                      '逍遥散': os.path.join(image_dir, "xiaoyaosan.png"),
                      '乾坤丹': os.path.join(image_dir, "qiankundan.png"),
                      '金疮药': os.path.join(image_dir, "jinchuangyao.png"),
                      '霞光宝塔': os.path.join(image_dir, "xiaguangbaota.png"),
                      }

    patterns = {
        r'收集物资': 'function_collect',
        r'捕捉': 'function_pet',
        r'援助': 'function_help',
        r'挑战': 'function_help',
        r'灵墟': 'function_help'# 71,108,484,320
    }
    @classmethod
    def shimen(cls):
        stop_event=threading.Event()
        t3 = threading.Thread(target=Daily_chumo.auto_incense, args=(stop_event,))
        t3.start()
        press_button('alt', 'y')
        time.sleep(1.2)
        todo_times = text_ocr.surplus_times('shimen')
        press_button('alt', 'y')
        stuck_threshold = 2
        stuck_count = 0
        cnt = 1
        while True:
            if stuck_count >= stuck_threshold:
                print(f"卡机超过{stuck_threshold}次，强制退出")
                stop_event.set()
                break
            if cnt % 5 ==0:
                press_button('alt', 'y')
                time.sleep(2)
                todo_times = text_ocr.surplus_times('shimen')
                press_button('alt', 'y')
            if todo_times <= 0:
                press_button('alt', 'y')
                time.sleep(2)
                todo_times = text_ocr.surplus_times('shimen')
                press_button('alt', 'y')
                if todo_times <= 0:
                    print('师门任务已完成，无法继续')
                    stop_event.set()
                    break
            print(f'师门还有{todo_times}环')
            task_text_list = text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144),text=None,click_or_not=False)
            task_text = ' '.join(task_text_list)
            found =False
            pattern_finish = r'.*?(修业)|.*?(修亚)'
            if re.search(pattern_finish, task_text) is None and todo_times<=0:
                print('师门已经完成，退出')
                stop_event.set()
                break
            if re.search(pattern_finish, task_text) is  None:
                print('领取师门任务')
                press_button('alt', 'y')
                time.sleep(1.2)
                locate_pos_click3('shimen')
                press_button('alt', 'y')
                cls.moving()
                time.sleep(1.2)
                text_ocr.ocr_target(region=(359,394,360,142),text='我要做任务',click_or_not=True)
                time.sleep(1.2)
            for pattern, function in cls.patterns.items():
                task_text_list = text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text=None,
                                                     click_or_not=False)
                task_text = ' '.join(task_text_list)
                core_match = re.search(r'【修业】.+', task_text)
                if core_match :
                    task_text = core_match.group()
                if match:= re.search(pattern,task_text):
                    print(f"匹配成功 - 模式: {pattern} → 函数: {function}")
                    cls.press_esc()
                    getattr(cls,function)()
                    found = True
                    todo_times -= 1
                    stuck_count = 0
                    cnt += 1
                    break
            if not found:
                print('检测出错，识别不到师门任务')
                stuck_count += 1
            else:
                stuck_count = 0
        time.sleep(3.5)

    @classmethod
    def function_collect(cls):
        pattern = r'.*?修业.*?收集物资(（完成）)|.*?修亚.*?收集物资(（完成）)'
        click_or_not = False
        while True:
            try:
                pattern_finish =r'.*?修业.*?(收集物资)|.*?修亚.*?(收集物资)'
                task_text_list = text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text=None,click_or_not=False)
                task_text = ' '.join(task_text_list).replace(' ','')
                time.sleep(1)
                if re.search(pattern_finish, task_text) is None:
                    print('收集已经完成，退出')
                    break
                if click_or_not:
                    break
                time.sleep(1)
                right_image_path = cls.return_article_image_path()
                for key in right_image_path:
                    print('师门买的物品',key)
                finish_or_not_list = text_ocr.ocr_target(region=(751, 144, 243,485),text=None,click_or_not=False)
                finish_or_not = ' '.join(finish_or_not_list).replace(' ','')
                finish_or_not = finish_or_not.replace('(','（')
                finish_or_not = finish_or_not.replace(')', '）')
                print(finish_or_not)
                match = re.search(pattern,finish_or_not)
                if match:
                    print('已完成购买，回门派')
                    time.sleep(0.5)
                    while True:
                        if text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144),text='修业',click_or_not=True):
                            break
                    human_like_move(504 + random.uniform(-30, 30), 709 + random.uniform(-30, 30))
                    cls.moving()  #赶路等待代码
                    time.sleep(1)
                    human_like_move(275 + random.uniform(-30, 30), 620 + random.uniform(-30, 30))
                    finish_or_not_list = text_ocr.ocr_target(region=(751, 144, 243, 485), text=None,
                                                             click_or_not=False)
                    finish_or_not = ' '.join(finish_or_not_list).replace(' ', '')
                    finish_or_not = finish_or_not.replace('(', '（')
                    finish_or_not = finish_or_not.replace(')', '）')

                    match2 = re.search(pattern, finish_or_not)
                    if match2 is None:
                        print('直接交付，无需点击了')
                        click_or_not = True
                        time.sleep(1.2)
                        cls.press_esc()
                        time.sleep(1)
                        break
                    else:
                        if text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144),text='修业',click_or_not=True):
                            print('已经有物品了')
                        if text_ocr.ocr_target(region=(355,400, 391,262),text='交任务',click_or_not=True):
                            print('交任务')
                            time.sleep(1)
                        if text_ocr.ocr_target(region=(355,400, 391,168),text='修业',click_or_not=True):
                            time.sleep(1)
                            print('进入交物品界面')
                        human_like_move(504+random.uniform(-5,5),709+random.uniform(-5,5))

                    time.sleep(0.5)
                    while True:
                        if click_or_not:
                            break
                        if cls.choose_article(right_image_path):
                            time.sleep(1)
                            cls.press_esc()
                            break
                        else:
                            continue
                else:
                    press_button('alt','j');time.sleep(1)
                    for _ in range(2):
                        time.sleep(0.5)
                        locate_pos_click3('goumai',region=(317,556,534,183))
                    press_button('alt', 'j')
            except Exception as e:
                pass

    @classmethod
    def function_pet(cls):
        pattern = r'.*?修业.*?捕捉宠物(（完成）)|.*?修亚.*?捕捉宠物(（完成）)'
        while True:
            time.sleep(1)
            finish_or_not_list = text_ocr.ocr_target(region=(751, 144, 243, 485), text=None, click_or_not=False)
            finish_or_not = ' '.join(finish_or_not_list).replace(' ','')
            finish_or_not = finish_or_not.replace('(', '（')
            finish_or_not = finish_or_not.replace(')', '）')
            match = re.search(pattern, finish_or_not)
            if match:
                text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='修业', click_or_not=True)
                text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='修亚', click_or_not=True)
                time.sleep(1.2)
                human_like_move(504 + random.uniform(-30, 30), 709 + random.uniform(-30, 30))
                cls.moving()
                time.sleep(1.2)
                cls.press_esc()
                break
            else:
                time.sleep(1.2)
                press_button('alt', 'e')
                time.sleep(1.2)
                if locate_pos_click3('dan',region=None,right_button='right',confidence=0.8) is False:
                    while True:
                        if locate_pos_click3('dan',region=None,right_button='right',confidence=0.8) is not False:
                            time.sleep(1)
                            break
                human_like_move(275 + random.uniform(-30, 30), 620 + random.uniform(-30, 30))
                time.sleep(1.2)
                text_ocr.ocr_target(region=(672,183,118,137),text='放入宠物',click_or_not=True)
                time.sleep(1.2)
                text_ocr.ocr_target(region=(468,481,233,168), text='宠物交易中心', click_or_not=True)
                time.sleep(1.2)
                text_ocr.ocr_target(region=(527,523, 233,77), text='信誉购买', click_or_not=True)
                time.sleep(1.2)
                cls.press_esc()


    @classmethod
    def function_help(cls):
        time.sleep(1)
        while True:
            time.sleep(1)
            if text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='修业', click_or_not=True):
                break
            if text_ocr.ocr_target(region=(751, 144, 986 - 751, 625 - 144), text='修亚', click_or_not=True):
                break
        time.sleep(1.2)
        human_like_move(504 + random.uniform(-30, 30), 709 + random.uniform(-30, 30))
        cls.moving()
        combat = False
        while True:
            time.sleep(5)
            combat_not =detect_combat_or_not()
            if combat_not and combat==False:
                print('进入师门援助战斗')
                press_button('ctrl', 'a')
                combat = True
            elif combat and combat_not is False:
                print('结束师门援助战斗')
                time.sleep(1.5)
                cls.press_esc()
                break
            elif combat==False and combat_not is False:
                print('无需战斗直接完成咯')
                cls.press_esc()
                break


    @classmethod
    def choose_article(cls, right_image_path):
        total_click_times = len(right_image_path)
        clicked_items=set()
        if text_ocr.detect_pic('beibao0'):
            locate_pos_click3('beibao0', region=(703, 204, 133, 247))
        for key, value in right_image_path.items():
            attempt = 0
            max_attempt = 15
            page = 0
            while attempt < max_attempt:
                time.sleep(1)
                if cls.article_click(value,confidence=0.7):
                    time.sleep(1)
                    clicked_items.add(key)
                    print(f'点击了{clicked_items}')
                    break
                else:
                    if attempt % 2 ==0:
                        _click = False
                        i = 0.6
                        for _ in range(2):
                            _click = cls.article_click(value,confidence=i)
                            time.sleep(1)
                            if _click:
                                clicked_items.add(key)
                                print('最里面的_click = cls.article_click(value,confidence=i)成功')
                                break
                            i-=0.1
                        if _click:
                            time.sleep(1)
                            print('_click = cls.article_click(value,confidence=i)成功')
                            break
                        else:
                            time.sleep(1)
                            print('_click = cls.article_click(value,confidence=i)未成功')
                    if attempt % 3 == 0:
                        print('去下一页寻找')
                        page += 1
                        if page > 2:
                            print('已经超过背包上限，重新进入')
                            page = 0
                        locate_pos_click3(f'beibao{page}')
                        time.sleep(1)
                    attempt += 1
        if total_click_times >= len(clicked_items):
            print('全部点击完成')
            text_ocr.ocr_target(region=(283, 499, 214, 156), text='确定', click_or_not=True)
            time.sleep(1)
            cls.press_esc()
            return True
        else:
            return False



    @classmethod
    def press_esc(cls):
        pyautogui.press('esc')
        time.sleep(1.2)
        if text_ocr.ocr_target_text(region=(276,478,478,187),text='游戏'):
            pyautogui.press('esc')


    @classmethod
    def moving(cls):
        cnt = 1
        print('赶路中')
        while True:
            RGB1 = text_ocr.moving_detect(region=(51,48,52,42))
            RGB3 = text_ocr.moving_detect(region=(651,103,52,42))
            if cnt %18 ==0:
                print('赶路中')
            time.sleep(2)
            cnt +=1
            RGB2 = text_ocr.moving_detect(region=(51,48,52,42))
            RGG4 = text_ocr.moving_detect(region=(651,103,52,42))
            if RGB1 == RGB2 or RGB3 == RGG4:
                break

    @classmethod
    def return_article_image_path(cls):  #任务栏文本返回需要点击物品的图片路径
        try:
            region = (751, 144, 986 - 751, 625 - 144)
            article_texts = text_ocr.ocr_target(region=region, text=None, click_or_not=False)
            #print('原始任务栏任务物品：',article_texts)
            clean_image_path =[]
            for text in article_texts:
                cleaned = re.sub(r'[^\u4e00-\u9fa5]', '', text)
                if cleaned:
                    clean_image_path.append(cleaned)
            clean_image_path = ' '.join(clean_image_path).replace(' ', '')
            clean_image_path = clean_image_path.replace('(', '（')
            clean_image_path = clean_image_path.replace(')', '）')
            print(f'师门1{clean_image_path}')
            star_word = clean_image_path.find('修业')
            end_key=star_word+25
            if star_word != -1:
                clean_image_path = clean_image_path[star_word:end_key]
            right_image_path={}
            print(f'师门2{clean_image_path},star_word={star_word}')
            for key,value in cls.article_to_pic.items():
                if key in clean_image_path:
                    right_image_path[key] = value
            print('师门点击的东西',right_image_path.items())
            return right_image_path
        except Exception as e:
            #print(f"选择物品异常: {str(e)}")
            return []


    @classmethod
    def article_click(cls,image_path,confidence=0.7): #物品点击代码
        try:
            box = pyautogui.locateOnScreen(image_path, region=(500,222,249,405), confidence=confidence)
            if box:
                pos = pyautogui.center(box)
                target_x, target_y = pos[0], pos[1]
                human_like_move(target_x, target_y)  # 使用曲线移动到目标位置
                pyautogui.click(x=target_x + random.uniform(-2, 2), y=target_y + random.uniform(-2, 2), button='Left')
                time.sleep(1)
                return True
            else:
                print("未找到图片，左键点击失败")
                return False
        except Exception as e:
            print(f"请稍等：{e}")
            return False




if __name__ == '__main__':
    move_window('高山流水')
    time.sleep(2)
    Daily_shimen.press_esc()



