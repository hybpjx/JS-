"""
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 #
# @Time    : 2022/4/18 14:19
# @Author  : zicliang
# @Email   : hybpjx@163.com
# @File    : log_conf.py
# @Software: PyCharm
"""
import datetime
import os
from loguru import logger

BASE_DIR = os.path.abspath("")
file_name = os.path.join(BASE_DIR, f'log/{datetime.date.today()}.log')

log_level = "ERROR"
# feature 字符串格式化
logger.add(
    file_name,
    enqueue=True,
    level=log_level,
    format="{message}——{level} | {time:YY年MM月DD日 HH时mm分}",
    encoding="utf-8",
    rotation="10 MB",
)
logger.opt(depth=1)

logger.info("项目开始启动。。。。")
