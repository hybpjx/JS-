# -*- coding: utf-8 -*-
# Copyright (C) 2021 #
# @Time    : 2021/12/15 10:35
# @Author  : zicliang
# @Email   : hybpjx@163.com
# @File    : Invoking.py
# @Software: PyCharm
import datetime
import time

from pydantic.types import date

from pkg.api_manager.script_api import APIManager
from pkg.api_manager.script_data import SpiderData
from pkg.exception.CustomException import TimeErrorException, UpdateSuccessException
from pkg.settings.log_conf import logger


class APIInvoke:

    def __init__(self, is_update: bool = True):
        # True 是允许数据重复 False 是不允许数据重复
        self.is_update = is_update
        self.API = APIManager()
        self.SPIDER = SpiderData()

    # 生成title id
    def data_update(self, api_data):
        try:

            api_data['title_date'] = self.SPIDER.getTitleDate(str(api_data['title_date']))

            # api_data['title_date'] = ''.join(api_data['title_date'])

            if len(api_data['title_name']) > 300:
                api_data['title_name'] = api_data['title_name'][:200]

        except TypeError as e:
            print(e)
            raise TimeErrorException(f"网站名为：{api_data['title_name']} 网站地址为：{api_data['site_path_url']} 日期校验失败")

        data = {
            # 网站 ID
            "site_id": api_data['site_id'],
            "title_name": api_data['title_name'],
            "title_url": api_data['title_url'],
            "content_html": str(api_data['content_html']),
            "title_date": api_data["title_date"],
            # "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),

            "site_name": api_data['site_name'],
            "site_type": api_data['title_type'],
            "site_path_name": api_data['site_path_name'],
            "site_path_url": api_data['site_path_url'],
            "title_source": api_data['site_name'],
            "update_user": "lzc",
        }
        try:
            self.Write_API(data)
        except UpdateSuccessException:
            return f"{data['site_id']}--{data['site_name']}--更新完毕"

    def Write_API(self, data):
        result = self.API.addDataToDB(data)
        self.API.updateConfigData(site_id=data['site_id'], run_status="正在更新", run_message="正在更新")

        if result[0] == 200:
            if self.is_update is False:
                logger.info(
                    f"\033[1;33m !!!{data['title_name'], data['title_date'], data['title_url']}>> 更新成功  !!! \n {result}")
                raise UpdateSuccessException("更新成功")
            else:
                logger.info(
                    f"\033[1;33m !!!{data['title_name'], data['title_date'], data['title_url']}>> 更新成功  !!! \n {result}")

        elif result[0] == 201:
            logger.info(
                f"\033[1;37m {data['title_name'], data['title_date'], data['title_url']}>> 添加成功 \n {result}")

        else:
            print(result)
            logger.critical(f"写入 API失败 请联系网站工作人员 {result}")
