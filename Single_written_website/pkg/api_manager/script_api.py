#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
====================================================================
Project Name: kyls_script
File description:
Author: Liao Heng
Create Date: 2022-07-28
====================================================================
"""
import time
import os
import socket
import platform
import datetime

from pkg.api_manager.api_request import APIRequest
from pkg.api_manager.script_data import SpiderData


class APIManager(object):
    def __init__(self):
        self.api_request = APIRequest()
        self.script_data = SpiderData()
        self.local_info = self.getLocalInfo()
        self.api_url_dict = {
            "目标网站": "http://admin.mykyls.com:18080/api/spider_data_config/",
            
            "拟在建项目": "http://admin.mykyls.com:18080/api/spider_nzj_data/",
            "政府部委": "http://admin.mykyls.com:18080/api/spider_zfbw_data/",
            "新闻媒体": "http://admin.mykyls.com:18080/api/spider_news_data/",
            "企业网站": "http://admin.mykyls.com:18080/api/spider_kscp_data/",
            "临时数据": "http://admin.mykyls.com:18080/api/spider_temp_data/",
            "采矿权": "http://admin.mykyls.com:18080/api/spider_ckq_data/",
            "探矿权": "http://admin.mykyls.com:18080/api/spider_tkq_data/",

            "目标企业": "http://admin.mykyls.com:18080/api/spider_qcc_config/",
            "企业新闻": "http://admin.mykyls.com:18080/api/spider_qcc_news/",
            "企业其他": "http://admin.mykyls.com:18080/api/spider_qcc_other/",
            "企业招标": "http://admin.mykyls.com:18080/api/spider_qcc_tender/",
        }

    def getLocalInfo(self):
        local_info = []
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        os_ver = platform.system()
        local_info.append("%s (%s) %s" % (hostname, local_ip, os_ver))
        local_info.append("%s" % os.getcwd())
        local_info.append("%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return "\n".join(local_info)

    def getApiUrl(self, table_name):
        if "政府" in table_name or "部委" in table_name:
            api_url = self.api_url_dict["政府部委"]
        elif "企业新闻" in table_name:
            api_url = self.api_url_dict["企业新闻"]
        elif "企业其他" in table_name:
            api_url = self.api_url_dict["企业其他"]
        elif "企业招标" in table_name:
            api_url = self.api_url_dict["企业招标"]
        elif "拟在建" in table_name:
            api_url = self.api_url_dict["拟在建项目"]
        elif "新闻" in table_name or "媒体" in table_name:
            api_url = self.api_url_dict["新闻媒体"]
        elif "企业" in table_name:
            api_url = self.api_url_dict["企业网站"]
        elif "采矿权" in table_name:
            api_url = self.api_url_dict["采矿权"]
        elif "探矿权" in table_name:
            api_url = self.api_url_dict["探矿权"]
        else:
            api_url = self.api_url_dict["临时数据"]
        return api_url

    def getConfigData(self, url_params={}):
        # 获取目标网站数据
        # run_status = ["错误", "等待更新", "正在更新", "结束"]
        api_url = self.api_url_dict["目标网站"]
        status, return_data = self.api_request.get(api_url, url_params)
        results = return_data.get("results", [])
        return results

    def updateConfigData(self, site_id, run_status="正在更新", run_message="运行中..."):
        # 更新目标网站数据
        run_status_list = ["错误", "等待更新", "正在更新", "结束"]
        if not site_id or run_status not in run_status_list:
            return 400, "updateConfigData error: site_id(%s) or run_status(%s)" % (site_id, run_status)
        config_data = self.getConfigData({"site_id": site_id})
        if config_data:
            config_data = config_data[0]
        else:
            return 400, "updateConfigData error: site_id %s" % site_id
        update_data = {
            'site_id': config_data['site_id'],
            'site_name': config_data['site_name'],
            "run_status": run_status,
            "run_message": self.local_info + "\n运行信息：%s" % run_message,
            "run_time": int(time.time())
        }
        api_url = self.api_url_dict["目标网站"] + str(config_data["id"]) + "/"
        api_data = self.api_request.put(api_url, update_data)
        return api_data

    def addDataToDB(self, title_dict={}):
        # 增加爬虫数据
        if not title_dict["site_name"] or not title_dict["site_type"] or not title_dict["site_id"]:
            return 400, {'status': False, 'detail': 'title_dict error'}
        api_url= self.getApiUrl(title_dict["site_type"])
        # 分析处理标题数据
        title_data = self.script_data.analysisTitleData(title_dict)
        # 发送数据到API
        # print(api_url)
        result = self.api_request.post(api_url, title_data)
        if result[0] not in [200, 201]:
            print(result)
        return result

    def getQccConfigData(self, url_params={}):
        # "目标企业": "http://admin.mykyls.com:18080/api/spider_qcc_config/",
        # "企业新闻": "http://admin.mykyls.com:18080/api/spider_qcc_news/",
        # "企业其他": "http://admin.mykyls.com:18080/api/spider_qcc_other/",
        # "企业招标": "http://admin.mykyls.com:18080/api/spider_qcc_tender/",
        # 获取目标网站数据
        # run_status = ["错误", "等待更新", "正在更新", "结束"]
        api_url = self.api_url_dict["目标企业"]
        status, return_data = self.api_request.get(api_url, url_params)
        results = return_data.get("results", [])
        return results

    def updateQccConfigData(self, qcc_id, run_status="正在更新", run_message="运行中..."):
        # 更新目标网站数据
        # run_status_list = ["错误", "等待更新", "正在更新", "结束"]
        if not qcc_id:
            return 400, "updateQccConfigData error: qcc_id(%s) or run_status(%s)" % (qcc_id, run_status)
        config_data = self.getQccConfigData({"qcc_id": qcc_id})
        if config_data:
            config_data = config_data[0]
        else:
            return 400, "updateConfigData error: qcc_id %s" % qcc_id
        update_data = {
            'qcc_id': config_data['qcc_id'],
            "run_status": run_status,
            "run_message": self.local_info + "\n运行信息：%s" % run_message,
            "run_time": int(time.time())
        }
        api_url = self.api_url_dict["目标企业"] + str(config_data["id"]) + "/"
        api_data = self.api_request.put(api_url, update_data)
        return api_data


if __name__ == "__main__":
    api = APIManager()
#     url_params = { "script_name": "script_qgj", "ordering": "run_time"}
#     data = api.getConfigData(url_params)
#     print(data)
#     # 正在更新
#     data = api.updateConfigData(site_id="6A4AA6F0FD", run_status="正在更新", run_message="正在更新")
#     print(data)
    title_data = {
        "title_id": "",          # 可以为空值
        "site_id": "6A4AA6F0FD", # 
        "site_name": "陕西省工业和信息化厅",
        "site_type": "企业其他",
        "site_path_name": "公告公示",
        "site_path_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/",
        "update_user": "",
    
        "title_date": "2022-08-27",
        "title_name": "测试数据",
        "title_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/qtgg/zfj/10636259671725203456.html",
        "content_html": '''<html><body><div>测试数据矿2022-01-27</body></html>''',
    }
    data = api.addDataToDB(title_data)
    print(data)
