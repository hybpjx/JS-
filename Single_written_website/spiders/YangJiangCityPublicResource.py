# -*- coding: utf-8 -*-
# @Time    : 2022/8/16 13:26
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : YangJiangCityPublicResource.py
# @Software: PyCharm
# https://ygp.gdzwfw.gov.cn/ggzy-portal/index.html#/441700/jygg
import hashlib
import execjs
import requests


class YangJiangCityPublicResource:

    def get_hash256(self, data: str):  # 对data加密
        hash256 = hashlib.sha256()
        hash256.update(data.encode('utf-8'))
        return hash256.hexdigest()

    def js_get_params(self):
        # 使用获取上下js2py生成一个上下文环境
        with open('../js/yangjiangshi.js', encoding='utf-8') as f:
            js_code = f.read()
        node = execjs.get()
        context = node.compile(js_code)
        headers_dict = context.eval("get_f()")
        c = context.eval("get_c()")
        return headers_dict, c

    def parse(self):
        headers, c = self.js_get_params()
        data = {"type": "trading-type", "publishStartTime": "", "publishEndTime": "", "siteCode": "441700",
                "secondType": "D", "projectType": "", "thirdType": "", "dateType": "", "total": 77, "pageNo": 1,
                "pageSize": 10, "openConvert": True}

        hash_str = headers[
                       'X-Dgi-Req-Nonce'] + c + \
                   f'dateType=&openConvert=true&pageNo={data["pageNo"]}&pageSize={data["pageSize"]}&projectType=&publishEndTime=&publishStartTime=&secondType={data["secondType"]}&siteCode={data["siteCode"]}&thirdType=&total={data["total"]}&type={data["type"]}' + \
                   headers['X-Dgi-Req-Timestamp']

        headers['X-Dgi-Req-Signature'] = self.get_hash256(hash_str)

        update_headers = {
            **headers,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://ygp.gdzwfw.gov.cn',
            'Referer': 'https://ygp.gdzwfw.gov.cn/ggzy-portal/index.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'X-Dgi-Req-App': 'ggzy-portal',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.post("https://ygp.gdzwfw.gov.cn/ggzy-portal/search/v1/items", json=data,
                                 headers=update_headers)
        print(response.text)


YangJiangCityPublicResource().parse()
