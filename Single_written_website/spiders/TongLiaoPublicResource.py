# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 9:58
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : TongLiaoPublicResource.py
# @Software: PyCharm
import ast
import base64
import re
from urllib.parse import urlencode, urljoin
import ddddocr
import fake_useragent
import requests
import ujson
from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke


class TongLiaoPublicResource:

    session = requests.session()
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": fake_useragent.UserAgent().random
        }

    def get_data(self, item, params):
        img_data = {
            "width": "150",
            "height": "40",
            "codeNum": "4",
            "interferenceLine": "4",
            "codeGuid": "",
        }
        resp = self.session.post(
            url="http://ggzy.tongliao.gov.cn/EpointWebBuilder_tlsggzy/jyxxInfoAction.action?cmd=getVerificationCode",
            headers=self.headers, data=img_data, timeout=5)
        img = resp.json()['custom']
        img_guid = ast.literal_eval(resp.json()['custom'])['verificationCodeGuid']
        # re.DOTALL 匹配多行
        result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)\"", img, re.DOTALL)
        if result:
            # 获得字典类型的结果
            ext = result.groupdict().get("ext")
            data = result.groupdict().get("data")
        else:
            raise Exception("Do not parse!")
        # 2、base64解码
        img_data = base64.urlsafe_b64decode(data)
        ocr = ddddocr.DdddOcr()
        res = ocr.classification(img_data)
        params['imgguid'] = img_guid
        params['yzm'] = res
        url = "http://ggzy.tongliao.gov.cn/EpointWebBuilder_tlsggzy/jyxxInfoAction.action?" + urlencode(params)
        response = self.session.post(url=url, headers=self.headers)
        for data in ujson.loads(response.json()['custom'])['Table']['JyxxInfoList']:
            #     # 目标的标题
            item['title_name'] = data['realtitle']
            #     # 目标详情页的地址
            item['title_url'] = urljoin(item['site_path_url'], data['infourl'])
            #     # # 目标日期
            item['title_date'] = data['infodate']
            item['content_html'] = self.session.get(url=item['title_url'], headers=self.headers).text
            APIInvoke().data_update(item)

    def run(self):
        source_list = [
            {
                "item": URL_DATA_INFO["TongLiaoPublicResource"][0],
                "params": {
                    "cmd": "getInfolist",
                    "fbdate": "",
                    "jyfrom": "",
                    "xxtype": "010",
                    "jytype": "",
                    "title": "",
                    "pageSize": "12",
                    "pageIndex": "0",
                    "imgguid": "",
                    "yzm": "",
                }
            },
            {
                "item": URL_DATA_INFO["TongLiaoPublicResource"][1],
                "params": {
                    "cmd": "getInfolist",
                    "fbdate": "",
                    "jyfrom": "",
                    "xxtype": "011",
                    "jytype": "",
                    "title": "",
                    "pageSize": "12",
                    "pageIndex": "0",
                    "imgguid": "",
                    "yzm": "",
                }
            },
            {
                "item": URL_DATA_INFO["TongLiaoPublicResource"][2],
                "params": {
                    "cmd": "getInfolist",
                    "fbdate": "",
                    "jyfrom": "",
                    "xxtype": "012",
                    "jytype": "",
                    "title": "",
                    "pageSize": "12",
                    "pageIndex": "0",
                    "imgguid": "",
                    "yzm": "",
                }
            },

        ]

        for item in source_list:
            self.get_data(item['item'], item['params'])


if __name__ == '__main__':
    TongLiaoPublicResource().run()
