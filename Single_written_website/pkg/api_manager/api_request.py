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
import json
import requests
import time
import socket


class APIRequest(object):
    """
    Description: 处理API请求
    """
    def __init__(self,):
        # spider/Linux@123
        self.header = {'Authorization': 'token d0b0ca6c686ceae342ecfe84425a5f481cb5d1de',
                       'Content-Type': 'application/json'}
        self.local_ip = self.getLocalIP()

    def getLocalIP(self):
        try:
            ip = ""
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
        except Exception:
            s.close()
        return ip

    def get(self, url, params={}, timeout=10):
        if "192.168.2" in self.local_ip:
            url = url.replace("admin.mykyls.com:18080", "192.168.2.107:18080")
        fail_count = 0
        while True:
            try:
                req = requests.get(url, params=params, headers=self.header, timeout=timeout)
                return req.status_code, req.json()
            except Exception as e:
                print("get error(%s): %s , %s" % (fail_count, url, str(e)))
            fail_count += 1
            if fail_count > 20:
                return 400, {"detail": str(e)}
            time.sleep(5)

    def delete(self, url, timeout=10):
        if "192.168.2" in self.local_ip:
            url = url.replace("admin.mykyls.com:18080", "192.168.2.107:18080")
        fail_count = 0
        while True:
            try:
                req = requests.delete(url, headers=self.header, timeout=timeout)
                result = req.json()
                return req.status_code, result
            except Exception as e:
                print("delete error: %s , %s" % (url, str(e)))
            fail_count += 1
            if fail_count > 20:
                return 400, {"detail": str(e)}
            time.sleep(5)

    def post(self, url, data, timeout=10):
        if "192.168.2" in self.local_ip:
            url = url.replace("admin.mykyls.com:18080", "192.168.2.107:18080")
        fail_count = 0
        while True:
            try:
                # print(data)
                req = requests.post(url, data=json.dumps(data), headers=self.header, timeout=timeout)
                result = req.json()
                return req.status_code, result
            except Exception as e:
                print(data)
                # print("post error:", data)
                # print("post error: %s , %s" % (url, str(e)))
            fail_count += 1
            if fail_count > 20:
                return 400, {"detail": str(e)}
            time.sleep(5)

    def put(self, url, data):
        if "192.168.2" in self.local_ip:
            url = url.replace("admin.mykyls.com:18080", "192.168.2.107:18080")
        fail_count = 0
        while True:
            try:
                req = requests.put(url, data=json.dumps(data), headers=self.header)
                result = req.json()
                return req.status_code, result
            except Exception as e:
                print("put error: %s , %s" % (url, str(data)))
                print("put error: %s , %s" % (url, str(e)))
            fail_count += 1
            if fail_count > 20:
                return 400, {"detail": str(e)}
            time.sleep(5)

    def test(self):
        url = "http://admin.mykyls.com:18080/api/spider_data_config/"
        url_params = { "site_id": "E26C9F69A5",}
        data = self.get(url, url_params)
        print(data)


if __name__ == "__main__":
    api = APIRequest()
    api.test()
