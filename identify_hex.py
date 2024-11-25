import get_list as glist
import easyocr
from PIL import ImageGrab
import cv2
import numpy as np
import re
from fuzzywuzzy import fuzz
from datetime import datetime


def capture_screen(a, b, c, d):
    """捕获‘选择一件’"""
    scaling_factor = 1  # 默认 win11, 1920*1080, 125% 缩放的屏幕，缩放因子为 0.8
    aa = a * scaling_factor
    bb = b * scaling_factor
    cc = c * scaling_factor
    dd = d * scaling_factor
    region = (aa, bb, cc, dd)
    screenshot = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
    return screenshot


def extract_text_from_image(image, reader):
    """从图像中提取文本，只识别中文"""
    # 将 PIL 图像转换为 numpy 数组
    image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # 使用 EasyOCR 进行文本识别
    results = reader.readtext(image_array, detail=0)
    # 仅保留中文字符
    results = [text for text in results if any('\u4e00' <= char <= '\u9fff' for char in text)]
    return results


def normalize_text(text):
    """标准化文本，去掉标点符号和额外的字符"""
    # 去掉标点符号和多余的空格
    text = re.sub(r'[^\w\s]', '', text)  # 去掉标点符号
    text = text.strip()
    return text


def identify_hexes(hex_number):
    """捕获屏幕并查找匹配条目"""
    reader = easyocr.Reader(['ch_sim'])  # 初始化 EasyOCR 读者
    my_cache_list = glist.get_list()  # 得到缓存列表

    count = 0  # 记录现在识别到第几个海克斯
    message = []  # 记录排名信息

    screenshot = capture_screen(430, 540, 1500, 570)
    texts = extract_text_from_image(screenshot, reader)  # 提取出的文本
    for text in texts:
        normalized_text = normalize_text(text)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 打印时间戳
        print(f"识别到'{normalized_text}'\t{current_time}")
        count += 1
        if count == hex_number:
            for item in my_cache_list:
                normalized_item = normalize_text(item)
                # 使用模糊匹配来比较
                if fuzz.partial_ratio(normalized_text, normalized_item) > 65:  # 80% 相似度阈值,投资++要65%，因为识别成了“投资十”
                    print(item)
                    message.append(f"{item}")
            return message
