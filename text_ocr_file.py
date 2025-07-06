import time
import pyautogui
from PIL import Image
import numpy as np
from io import BytesIO
import random
import re
import os
from main import human_like_move


class text_ocr:
    _ocr_engine = None
    all_ocr_cache = {}
    cache_duration = 1
    MAX_CACHE_SIZE = 10000
    @staticmethod
    def get_ocr(lang='ch'):
        if not text_ocr._ocr_engine or lang != text_ocr._current_lang:
            from paddleocr import PaddleOCR
            text_ocr._ocr_engine = PaddleOCR(use_angle_cls=True, lang=lang)
            text_ocr._current_lang = lang
        return text_ocr._ocr_engine

    @staticmethod
    def ocr_target(region, text ,click_or_not = False):
        try:
            with BytesIO() as buffer:
                pyautogui.screenshot(region=region).save(buffer,format='PNG')
                buffer.seek(0)
                img = Image.open(buffer)
                img_array = np.array(img.convert('RGB'))
            ocr = text_ocr.get_ocr()
            if ocr is None:
                print("OCR引擎未初始化!")
                return [] if not click_or_not else False
            result = ocr.ocr(img_array,cls=True)
            if click_or_not:
                x1, y1, length, width = region
                for line in result[0]:
                    if text in line[1][0]:
                        points = np.array(line[0], dtype=np.int32)
                        center_x = int(points[:, 0].mean())
                        center_y = int(points[:, 1].mean())
                        real_x1 = x1 + center_x + random.uniform(-3,3)
                        real_y1 = y1 + center_y + random.uniform(-3,3)
                        human_like_move(real_x1,real_y1)
                        pyautogui.click(real_x1,real_y1)
                        return True
                return False
            else:
                texts = []
                for line in result[0]:
                    texts.append(line[1][0])
                return [line[1][0] for line in result[0]]

        except Exception as e:
                return [] if not click_or_not else False

    @staticmethod
    def ocr_target_text(region, text):
        try:
            with BytesIO() as buffer:
                pyautogui.screenshot(region=region).save(buffer, format='PNG')
                buffer.seek(0)
                img = Image.open(buffer)
                img_array = np.array(img.convert('RGB'))
            ocr = text_ocr.get_ocr()
            result = ocr.ocr(img_array, cls=True)
            if not result or not result[0]:
                return  False
            for line in result[0]:
                if text in line[1][0]:
                    return True
            return False

        except Exception as e:
            return False




    @staticmethod
    def surplus_times(task_pic): #日常面板检测任务剩余数量
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'picture', f"{task_pic}.png")
        try:
            box = pyautogui.locateOnScreen(image_path, confidence=0.7)
            if box is None:
                print("未能找到图片坐标，请检查图片是否正确")
                return 0
            else:
                pos = pyautogui.center(box)
                x1 , y1 =int(pos[0])-38, int(pos[1])
                texts = text_ocr.ocr_target(region=(x1,y1,87,52),text=None,click_or_not = False)
                match_pattern = r"(\d+)\s*/\s*(\d+)"
                for text in texts:
                    text = text.replace("O", "0").replace("o", "0")
                    match = re.search(match_pattern, text)
                    if match:
                        current_times=int(match.group(1))
                        total_times=int(match.group(2))
                        return total_times-current_times
                print(f"未找到进度信息，请检查原因")
                return 0

        except Exception as e:
            print(f"识别任务次数失败:，原因：{e}")
            return 0
        
    @staticmethod
    def detect_pic(pic, region=None): #检测目标图片是否存在
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, 'picture', f"{pic}.png")
            box = pyautogui.locateOnScreen(image_path, confidence=0.7, region=region)
            if box:
                pos = pyautogui.center(box)
                return pos
            else:
                return False
        except Exception as e:
            return False


    @staticmethod
    def rounde_number(category_renwu):
                try:
                    region = (751, 144, 986 - 751, 625 - 144)
                    texts = text_ocr.ocr_target(region=region, text=None, click_or_not=False)
                    if texts is None:
                        processed_text = ""
                    elif isinstance(texts, list):
                        processed_text = "".join([str(t) for t in texts if t is not None])
                    else:
                        processed_text = str(texts)
                    safe_category = re.escape(category_renwu)
                    pattern = rf"【{safe_category}】.*?第(\d+)环"
                    match = re.search(pattern, processed_text, flags=re.DOTALL)
                    if match:
                        return int(match.group(1))
                    else:
                        return 0
                except Exception as e:
                    return 0

    @staticmethod
    def moving_detect(region=None):
        try:
            screenshot = pyautogui.screenshot(region=region)
            temp_image = BytesIO()
            screenshot.save(temp_image, format="PNG")
            temp_image.seek(0)
            with Image.open(temp_image) as img:
                img = img.convert('RGB')
                center_x = img.width // 2
                center_y = img.height // 2
                pixels = []
                for x in range(center_x - 12, center_x + 13, 2):
                    for y in range(center_y - 12, center_y + 13, 2):
                        pixels.append(img.getpixel((x, y)))
                total_pixels = len(pixels)
                avg_r = sum(p[0] for p in pixels) // total_pixels
                avg_g = sum(p[1] for p in pixels) // total_pixels
                avg_b = sum(p[2] for p in pixels) // total_pixels
                return avg_r, avg_g, avg_b

        except Exception as e:
            pass

    @staticmethod
    def move_or_not():
        RGB1 = text_ocr.moving_detect(region=(51, 48, 52, 42))
        RGB3 = text_ocr.moving_detect(region=(651, 103, 52, 42))
        time.sleep(2)
        RGB2 = text_ocr.moving_detect(region=(51, 48, 52, 42))
        RGG4 = text_ocr.moving_detect(region=(651, 103, 52, 42))
        if RGB1 == RGB2 or RGB3 == RGG4:
            return False
        else:
            return True

    @staticmethod
    def level_info():
        try:
            region = (513,183,178,214)
            texts = text_ocr.ocr_target(region=region, text=None, click_or_not=False)
            if texts is None:
                processed_text = ""
            elif isinstance(texts, list):
                processed_text = "".join([str(t) for t in texts if t is not None])
            else:
                processed_text = str(texts)
            pattern = r"等级\s*(\d+)\s*级"
            match = re.search(pattern, processed_text, flags=re.DOTALL)
            if match:
                return int(match.group(1))
            else:
                return 0

        except Exception as e:
            return 0

    @staticmethod
    def longhun_times():
        try:
            region=(173,150,412,188)
            texts = text_ocr.ocr_target(region=region, text=None, click_or_not=False)
            if texts is None:
                processed_text = ""
            elif isinstance(texts, list):
                processed_text = "".join([str(t) for t in texts if t is not None])
            else:
                processed_text = str(texts)
            pattern = r"获得一次免费刷新机会([\u4e00-\u9fa5]{2})刷新"
            match = re.search(pattern, processed_text, flags=re.DOTALL)
            #print(f'{processed_text}||{match.group(1)}')
            if match and match.group(1) == '免费' :
                return True
            else:
                return False
        except Exception as e:
            return 0

    @staticmethod
    def longhun_goumai():
        try:
            region = (513, 183, 178, 214)
            texts = text_ocr.ocr_target(region=region, text=None, click_or_not=False)
            if texts is None:
                processed_text = ""
            elif isinstance(texts, list):
                processed_text = "".join([str(t) for t in texts if t is not None])
            else:
                processed_text = str(texts)
            pattern = r"等级\s*(\d+)\s*级"
            match = re.search(pattern, processed_text, flags=re.DOTALL)
            if match:
                return int(match.group(1))
            else:
                return 0

        except Exception as e:
            return 0



if __name__ == "__main__":
    pass



