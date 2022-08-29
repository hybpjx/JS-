# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 14:10
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : China_BulletinList.py
# @Software: PyCharm

import binascii
import json
import time

import requests
import pyDes
import urllib3  # 解除InsecureRequestWarning警告
from tqdm import tqdm

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 解除InsecureRequestWarning警告


class ChinaBulletinList:
    def __init__(self):
        self.item = {'site_path_name': URL_DATA_INFO["China_BulletinList"]["site_path_name"],
                     'site_id': URL_DATA_INFO["China_BulletinList"]["site_id"],
                     'site_path_url': URL_DATA_INFO["China_BulletinList"]["site_path_url"],
                     'site_name': URL_DATA_INFO["China_BulletinList"]["site_name"],
                     'title_type': URL_DATA_INFO["China_BulletinList"]["title_type"],
                     'title_source': URL_DATA_INFO["China_BulletinList"]["title_source"],
                     }
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'custominfo.cebpubservice.com',
            'Origin': 'http://ctbpsp.com',
            'Referer': 'http://ctbpsp.com/',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        # https://custominfo.cebpubservice.com/cutominfoapi/searchkeyword?keyword=%E7%A3%81%E9%80%89&uid=0&PageSize=10&CurrentPage=1&searchType=0&bulletinType=5
        # https://valbr.bangruitech.com/asValidate?authId=ihW-SBA9454j_c1GKeqTZBnmn8aLITgV&rank=3&signId=173&ts=1656056271559&uuid=wBtWBuFPolkp5aMQJ1B1AZZWoIt-dMwy&vid=4&hashCode=bD0_7J1t8EBFtINQ8_SxJohRAmaVivnjgUER9PO_sPaDIVOkK_UhO_ComNqHgug7835Jy4KeO5VUvEcpy4gZBux4D-1Fjc9cf5KmKgT1ydOKoQoj3ZW9Uy1LeZCe4t-c14ms1uGdglJ9afe0aPpas9w5dqwN4Y6I&returnUrl=
        self.API = APIInvoke()

    def decrypt_data(self, url, params):
        """
        传入链接和参数

        然后得到数据
        解析数据
        返回数据
        """
        # 代理
        proxy = {
            # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
            'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
        }
        # 解析数据 得到响应
        response = self.session.get(url=url,
                                    params=params,
                                    headers=self.headers,
                                    proxies=proxy,
                                    verify=False)
        # 去除 双引号 用切片的方式
        page_text = response.text[1:-1]

        # 如果不是加密数据 则判断为有验证码 即已被反爬
        if "html lang=\"en\"" in page_text:
            print("对方服务器对您进行了拦截")
            # return False
        time.sleep(3)
        # 解析原来的数据 base64解密
        data = binascii.a2b_base64(page_text)
        key = "ctpstp@custominfo!@#qweASD"[0:8]
        des_obj = pyDes.des(key=key, mode=pyDes.ECB, padmode=pyDes.PAD_PKCS5)
        text = des_obj.decrypt(data).decode("utf-8")

        return text

    def get_data(self):
        keywords = [
            "磁选",
            "矿", "立磨", "塔磨", "辊压", "磁选", "砂石骨料", "旋流器",
            "渣浆泵", "球团", "高岭土", "浮选", "地质", "钢球", "碳中和", "废钢", "炉料",
        ]
        for key in tqdm(keywords):
            params = {
                "keyword": key,
                "uid": "0",
                "PageSize": "100",
                "CurrentPage": "1",
                "searchType": "0",
                "bulletinType": "5",
            }
            html_text = self.decrypt_data("https://custominfo.cebpubservice.com/cutominfoapi/searchkeyword", params)
            self.item_get(html_text)

        self.close_session()

    def get_all_data(self):

        url_list = [
            "https://custominfo.cebpubservice.com/cutominfoapi/recommand/type/5/pagesize/10/currentpage/{}".format(i)
            for i in range(1, 10)]
        for url in url_list:
            html_text = self.decrypt_data(url, {})

            self.item_get(html_text)

        self.close_session()

    def item_get(self, html_text):
        for data in json.loads(html_text)['data']['dataList']:
            self.item['title_name'] = str(data['noticeName']).replace("<em>", "").replace("</em>", "")
            self.item['title_url'] = 'https://ctbpsp.com/#/bulletinDetail?uuid=' + data['bulletinID']

            self.item['title_date'] = data['noticeSendTime']
            time.sleep(15)
            content_html = self.decrypt_data(
                f"https://custominfo.cebpubservice.com/cutominfoapi/bulletin/{data['bulletinID']}/uid/0", params={})
            json_text = json.loads(content_html)
            try:
                content_url = json_text['data']['pdfUrl']
                self.item['content_html'] = f'<embed type="text/html" src="{content_url}" width="100%" height="1000px">'
            except TypeError:
                self.item['content_html'] = "详情页获取失败 请手动查看原文链接"

            self.API.data_update(self.item)

    def close_session(self):
        self.session.close()


if __name__ == '__main__':
    cbl = ChinaBulletinList()
    cbl.get_data()
