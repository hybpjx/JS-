# -*- coding: utf-8 -*-
# @Time    : 2022/7/13 9:34
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : YuanBoWeb.py
# @Software: PyCharm

# https://www.chinabidding.cn/public/2020/html/zbcglist.html
import time
import execjs
import json
import requests
from urllib.parse import urljoin
from pyquery import PyQuery as pq

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke


class YuanBoWeb:
    base_url = "https://www.chinabidding.cn/yuan/zbcg/ZbcgChannel/getDataList"
    session = requests.session()

    URL_DATA_INFO_TYPE = "YuanBoWeb"
    item = {
        'site_path_name': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_path_name'],
        'site_id': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_id'],
        'site_path_url': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_path_url'],
        'site_name': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_name'],
        'title_type': URL_DATA_INFO[URL_DATA_INFO_TYPE]['title_type'],
        'title_source': URL_DATA_INFO[URL_DATA_INFO_TYPE]['title_source'],
    }
    with open('../js/YuanBo.js', 'r', encoding='utf-8') as fp:
        js_text = fp.read()
    API = APIInvoke()

    def parse(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

        for i in range(4):
            params = {
                "key": "机械 / 设备",
                "search_key": "4000338",
                "table_type": "4",
                "page": str(i + 1),
            }
            response = self.session.get(self.base_url, headers=headers, params=params)
            ctx = execjs.compile(self.js_text)
            data = ctx.eval("convert3('{}')".format(response.text))

            json_text = json.loads(data)
            for j in json_text['list']:
                self.item['title_name'] = j['title']
                self.item['title_date'] = j.get('date')
                self.item['title_url'] = urljoin(self.base_url, j.get('url'))
                if self.item['title_date'] is None:
                    self.item['title_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                self.item['content_html'] = pq(self.session.get(self.item['title_url'], headers=headers).text)(
                    "#main_dom")
                # main_dom
                self.API.data_update(self.item)

        self.close()

    def close(self):
        self.session.close()



if __name__ == '__main__':
    YuanBoWeb().parse()
