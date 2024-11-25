import os
from datetime import datetime

date_file = 'last_run_date.txt'  # 用于保存上次运行日期的文件


def has_run_today():
    """检查今天是否已经运行过"""
    if os.path.exists(date_file):
        with open(date_file, 'r') as file:
            last_run_date = file.read().strip()
            # 获取当前日期字符串
            today = datetime.now().strftime('%Y-%m-%d')
            return last_run_date == today
    return False


def update_run_date():
    """更新运行日期为今天"""
    with open(date_file, 'w') as file:
        today = datetime.now().strftime('%Y-%m-%d')
        file.write(today)
