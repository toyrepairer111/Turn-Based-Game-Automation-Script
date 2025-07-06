import win32process
from win32process import GetWindowThreadProcessId
import pyautogui
import os
import time
import win32gui
from PIL import Image
from io import BytesIO
import tempfile
import sys
from contextlib import contextmanager
from io import StringIO
from pynput.mouse import Controller
import random
import numpy as np
from paddleocr import PaddleOCR
import asyncio
import math
from pynput import keyboard


mouse = Controller()
import numpy as np
import pyautogui
import random
import time


def ease_out_quad(t):
    return 1 - (1 - t) ** 2

def cubic_bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u ** 3 * p0[0] + 3 * u ** 2 * t * p1[0] + 3 * u * t ** 2 * p2[0] + t ** 3 * p3[0],
        u ** 3 * p0[1] + 3 * u ** 2 * t * p1[1] + 3 * u * t ** 2 * p2[1] + t ** 3 * p3[1]
    )

def human_like_move(target_x, target_y,target_offset=5):
    final_x = target_x + random.randint(-target_offset, target_offset)
    final_y = target_y + random.randint(-target_offset, target_offset)
    # 获取当前鼠标位置
    start_x, start_y = pyautogui.position()
    distance = ((target_x - start_x) ** 2 + (target_y - start_y) ** 2) ** 0.5

    # 根据距离确定步数
    min_steps = max(50, int(distance * 0.3))
    max_steps = max(80, int(distance * 0.5))
    steps = random.randint(min_steps, max_steps)

    # 计算控制点，使用随机偏移使路径更自然
    max_offset = int(distance * 0.1)
    control1 = (
        (start_x + target_x) // 2 + random.randint(-max_offset, max_offset),
        (start_y + target_y) // 2 + int(random.gauss(0, max_offset / 2))
    )
    control2 = (
        (start_x + target_x) // 2 + int(random.gauss(0, max_offset / 3)),
        (start_y + target_y) // 2 + random.randint(-max_offset, max_offset)
    )

    # 生成缓动后的t值列表和对应的贝塞尔曲线路径点
    t_values = [ease_out_quad(t) for t in np.linspace(0, 1, steps)]
    points = []
    for t in t_values:
        x, y = cubic_bezier(
            (start_x, start_y),
            control1,
            control2,
            (final_x, final_y),  # 使用偏移后的终点
            t
        )
        points.append((int(x), int(y)))

    try:
        # 提升pyautogui的精度
        pyautogui.MINIMUM_SLEEP_TIME = 0.001
        pyautogui.MINIMUM_DURATION = 0.01

        # 按顺序依次移动鼠标

        for x, y in points:
            duration = random.uniform(0.01, 0.015) * distance / 1000
            pyautogui.moveTo(x, y, duration=duration, _pause=False)
            # 随机小停顿，增加自然感
            if random.random() < 0.3:
                time.sleep(random.uniform(0.001, 0.008))
    finally:
        # 确保最后定位到目标点，并恢复默认参数
        pyautogui.MINIMUM_SLEEP_TIME = 0.1

def locate_pos_click2(image_name, region=None, offset_x=None, offset_y=None, confidence=0.7):
    try:
        folders = ['picture', 'renwuwupin']
        image_path = find_pic_in_folders(image_name, folders)
        Box = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        if Box is not None:
            pos = pyautogui.center(Box)
            target_x, target_y = pos[0], pos[1]
            human_like_move(target_x, target_y)  # 使用曲线移动到目标位置
            pyautogui.click(button='Left')
        else:
            print("未找到")
    except Exception as e:
        print(f"locate_pos_click2发生错误：{e}")

def locate_pos_click3(image_name, region=None,right_button=None,confidence = 0.7):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'picture', f"{image_name}.png")
        box = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        if box:
            pos = pyautogui.center(box)
            target_x, target_y = pos[0], pos[1]
            human_like_move(target_x, target_y)  # 使用曲线移动到目标位置
            if right_button:
                pyautogui.click(x=target_x+ random.uniform(-2,2), y=target_y+ random.uniform(-2,2),button='Right')
            else:
                pyautogui.click(x=target_x+ random.uniform(-2,2), y=target_y+ random.uniform(-2,2),button='Left')

        else:
            print("未找到图片，左键点击失败")
            return False
    except Exception as e:
        print(f"请稍等：{e}")
        return False

def locate_pos_click(confidence_num):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path2 = os.path.join(script_dir, 'picture', "baotu.png")
    cnt = 0
    while True:
        for i in range(10):
            image_name = f"num{i}.png"
            image_path = os.path.join(script_dir, 'picture', image_name)
            print("开始寻找")
            try:
                Box = pyautogui.locateOnScreen(image_path, confidence=confidence_num)

                if Box is not None:
                    pos = pyautogui.center(Box)
                    print(f"成功获取图片位置{pos}")

                    # 取消点击偏移，直接点击目标中心
                    target_x, target_y = pos[0], pos[1]

                    human_like_move(target_x, target_y)  # 使用曲线移动到目标位置
                    pyautogui.click(button='Left')
                    time.sleep(random.uniform(0.1, 0.5))
                    print(f"点击位置({target_x}, {target_y})成功")
                elif cnt > 10:
                    break
                else:
                    print("未找到")
            except Exception as e:
                print("未在界面中找到")
                cnt += 1
                continue
        try:
            Box2 = pyautogui.locateOnScreen(image_path2, confidence=confidence_num)
            if Box2 is not None:
                pos2 = pyautogui.center(Box2)
                print(f"成功获取图片位置{pos2}")

                # 取消点击偏移，直接点击目标中心
                target_x, target_y = pos2[0], pos2[1]

                human_like_move(target_x, target_y)  # 使用曲线移动到目标位置
                pyautogui.click(button='Right')
                time.sleep(random.uniform(0.1, 0.5))
                human_like_move(1023, 579)  # 随机移动到某个固定点
                print(f"点击位置({target_x}, {target_y})成功")
            else:
                print("未找到")
        except Exception as e:
            print("未在界面中找到")
            continue

def find_pic_in_folders(pic, folders):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for each in folders:
        path = os.path.join(script_dir, each, pic)
        if os.path.exists(path):
            return path
    return None


async def pet_monitor():
    while True:
        try:
            if bb_dead():
                print('宠物死亡，执行召唤操作')
                await asyncio.to_thread(locate_pos_click2, 'zhaohuan.png', region=(841, 311, 148, 95))
                await asyncio.sleep(0.8)
                await asyncio.to_thread(locate_pos_click2, 'zhaohuan2.png')
            await asyncio.sleep(1)  # 每1秒检测一次
        except Exception as e:
            print(f"宠物监控异常: {str(e)}")

def bb_dead(region=(800, 40, 36, 37)):
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
            for x in range(center_x - 12, center_x + 13,2):
                for y in range(center_y - 12, center_y + 13,2):
                    pixels.append(img.getpixel((x, y)))
            total_pixels = len(pixels)
            avg_r = sum(p[0] for p in pixels) // total_pixels
            avg_g = sum(p[1] for p in pixels) // total_pixels
            avg_b = sum(p[2] for p in pixels) // total_pixels
            is_gray = (abs(avg_r - avg_g) < 5) and (abs(avg_g - avg_b) < 5)
            if is_gray: # 允许一定误差
                return True
            else:
                return False

    except Exception as e:
        pass



def detect_combat_or_not():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'picture', "huihe.png")
        box = pyautogui.locateOnScreen(
            image_path,
            region=(655, 47, 253, 125),
            confidence=0.7
        )
        if box:
            return True
        else:
            return False
    except Exception as e:
        return False


def detect_combat_no_async():

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'picture', "huihe.png")


        box = pyautogui.locateOnScreen(
            image_path,
            region=(655, 47, 253, 125),
            confidence=0.7
        )

        if box is None:
            return False

        print('进入战斗')
        cnt=1
        while True:
            cnt +=1;time.sleep(0.1)
            if bb_dead():
                print('宠物死亡，执行召唤操作')
                locate_pos_click3('zhaohuan', region=(841, 311, 148, 95))
                time.sleep(0.8)
                locate_pos_click3('zhaohuan2')
            if cnt >=300:
                break
            press_button('ctrl', 'a')
            pyautogui.screenshot(region=(655, 47, 253, 125))


            for _ in range(25):
                time.sleep(1)
                if bb_dead():
                    print('宠物死亡，执行召唤操作')
                    locate_pos_click3('zhaohuan', region=(841, 311, 148, 95))
                    time.sleep(0.8)
                    locate_pos_click3('zhaohuan2')


            current_box = pyautogui.locateOnScreen(
                image_path,
                region=(655, 47, 253, 125),
                confidence=0.7
            )
            if current_box is None:
                print('结束战斗')
                return False

    except Exception as e:
        pass
        return False

async def detect_combat():
    try:

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'picture', "huihe.png")
        Box = await asyncio.to_thread(
            pyautogui.locateOnScreen,
            image_path,
            region=(655, 47, 253, 125),
            confidence=0.7
        )
        if Box :
            print('进入战斗')
            pet_task = asyncio.create_task(pet_monitor())
            while True:
                Box = await asyncio.to_thread(
                    pyautogui.locateOnScreen,
                    image_path,
                    region=(655, 47, 253, 125),
                    confidence=0.7
                )
                if Box is None:
                    print('结束战斗')
                    pet_task.cancel()
                    return False
                await asyncio.to_thread(press_button, 'ctrl', 'a')
                await asyncio.to_thread(pyautogui.screenshot, region=(655, 47, 253, 125))
                await asyncio.sleep(25)
                print('继续战斗')
        else:
            return False
    except Exception as e:
        return False

def press_button(left, right):
    pyautogui.keyDown(f'{left}') # 按下 Alt 键
    pyautogui.press(f'{right}') # 按下 Y 键
    pyautogui.keyUp(f'{left}') # 松开 Alt 键

def detect_picture2(pic, region=None, position=None, confidence=0.7):
    try:
        folders = ['picture', 'renwuwupin']
        image_path = find_pic_in_folders(pic, folders)
        Box = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
        print(Box)
        if Box is not None:
            if position is not None:
                pos = pyautogui.center(Box)
                return pos
            return True
        else:
            print('已经点击关闭')
            return False
    except Exception as e:
        print(f"{e}")
        print('错误')
        return False

def wen_jian():
    try:
        from text_ocr_file import text_ocr
        press_button('alt', 'y')
        todo_times = text_ocr.surplus_times('lingyan');time.sleep(1)
        print(f'凌烟任务还剩{todo_times}次'), time.sleep(0.1)
        press_button('alt', 'y')
        if todo_times == 0:
            print('凌烟任务已经完成，无法继续')
            return
        for i in range(todo_times):
            press_button('alt', 'y')
            locate_pos_click3('wenjian')
            time.sleep(0.5)
            locate_pos_click3('tiaozhan', region=(365,411, 104, 108))
            time.sleep(0.5)
            while True:
                if text_ocr.ocr_target(region=(346,350,359,153),text='确定',click_or_not=True):
                    locate_pos_click3('queren', region=(346, 350, 359, 153))
                    break
            press_button('ctrl', 'a')
            time.sleep(8)
            while True:
                if detect_combat_no_async() is False:
                    break
            if i == todo_times-1:
                print('凌烟任务已经完成')
                time.sleep(0.7)
                pyautogui.press('esc')
                time.sleep(0.7)
                pyautogui.press('esc')
    except Exception as e:
        print(f"发生错误: {e}")

def find_game_handle():
    pid = 16736 # 每次都会改变

    def callback(hwnd, hwnds):
        if all([GetWindowThreadProcessId(hwnd)[1] == pid, win32gui.IsWindowVisible(hwnd)]):
            print(win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd))

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)

def find_handle(game_area):
    hwnd = win32gui.FindWindow('GLFW30', f'幻唐志 - {game_area}')
    rect = win32gui.GetWindowRect(hwnd) # 获取当前窗口的位置和大小
    width = rect[2] - rect[0] # 计算宽度
    height = rect[3] - rect[1] # 计算高度
    return hwnd, width, height

def find_handle2():
    hwnd = win32gui.FindWindow('GLFW30', f'幻唐志')
    rect = win32gui.GetWindowRect(hwnd) # 获取当前窗口的位置和大小
    width = rect[2] - rect[0] # 计算宽度
    height = rect[3] - rect[1] # 计算高度
    return hwnd, width, height

def move_window2():
    hwnd, width, height = find_handle2()
    win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
    print(f"获取句柄成功,句柄为{hwnd},大小为{width}'*'{height}")
    time.sleep(0.1)
    pyautogui.click(x=551+random.uniform(-10,10), y=448+random.uniform(-10,10), button='Left')

def move_window(game_area):
    hwnd, width, height = find_handle(game_area)
    win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
    print(f"获取句柄成功,句柄为{hwnd},大小为{width}'*'{height}")
    time.sleep(0.1)
    pyautogui.click(x=513+random.uniform(-30,50), y=403+random.uniform(-50,100), button='Left')


def move_window_3(game_area):
    hwnd, width, height = find_handle(game_area)
    win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
    print(f"获取句柄成功,句柄为{hwnd},大小为{width}'*'{height}")
    time.sleep(0.1)
    pyautogui.click(x=513+random.uniform(-10,10), y=403+random.uniform(-10,10), button='Right')

    #from shimen import Daily_shimen
    #Daily_shimen.press_esc()




def dig_treasure(game_area):
    move_window(game_area)
    locate_pos_click(.7)

def find_pic(all_situation):
    try:
        for pic in all_situation:
            if detect_picture2(pic, region=(727, 165, 264, 329), confidence=0.9):
                print(f'执行的是{pic}任务')
                return pic
            else:
                print('未识别到任务')
                return False
    except Exception as e:
        print(f"{e}")


async def async_guaji(game_area):
    move_window(game_area)
    while True:
        print("[挂机状态] 持续检测战斗...")
        await detect_combat()
        await asyncio.sleep(1)

async def async_guaji2():
    move_window2()
    while True:
        print("[挂机状态] 持续检测战斗...")
        await detect_combat()
        await asyncio.sleep(1)


def get_all_windows():
    """获取所有可见窗口的句柄和标题"""
    windows = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            windows.append((hwnd, title, class_name, pid))

    win32gui.EnumWindows(callback, None)
    return windows

if __name__ == "__main__":
    print('program is running')
    #dig_treasure('风驰电掣')
    #Wen_jian('风云再起')
    #move_window('风云再起')
    #hwnd = win32gui.FindWindow('GLFW30', f'幻唐志')
    #print(hwnd)
    asyncio.run(async_guaji2()) #乐斗挂机专用
    #dig_treasure('风云再起')
    #asyncio.run(async_guaji('高山流水'))  #平常挂机专用


