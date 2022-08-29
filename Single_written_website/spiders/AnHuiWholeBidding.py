# -*- coding: utf-8 -*-
# @Time    : 2022/8/26 10:47
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : AnHuiWholeBidding.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 15:45
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : test1.py
# @Software: PyCharm
from urllib.parse import urljoin

import requests
import re
import execjs
import hashlib
import json
from requests.utils import add_dict_to_cookiejar
from scrapy.selector import Selector

from pkg.Invoking import APIInvoke


class AnHuiWholeBidding:
    url = 'https://www.bidnews.cn/caigou/search-htm-page-2-stype-fuwu.html'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    API = APIInvoke()

    @staticmethod
    def getCookie(data):
        """
        通过加密对比得到正确cookie参数
        :param data: 参数
        :return: 返回正确cookie参数
        """
        chars = len(data['chars'])
        for i in range(chars):
            for j in range(chars):
                clearance = data['bts'][0] + data['chars'][i] + data['chars'][j] + data['bts'][1]
                encrypt = None
                if data['ha'] == 'md5':
                    encrypt = hashlib.md5()
                elif data['ha'] == 'sha1':
                    encrypt = hashlib.sha1()
                elif data['ha'] == 'sha256':
                    encrypt = hashlib.sha256()
                encrypt.update(clearance.encode())
                result = encrypt.hexdigest()
                if result == data['ct']:
                    return clearance

    def get_text(self, url):
        # 使用session保持会话
        session = requests.session()
        res1 = session.get(url, headers=self.header)
        jsl_clearance_s = re.findall(r'cookie=(.*?);location', res1.text)[0]
        # 执行js代码
        jsl_clearance_s = str(execjs.eval(jsl_clearance_s)).split('=')[1].split(';')[0]
        # add_dict_to_cookiejar方法添加cookie
        add_dict_to_cookiejar(session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
        res2 = session.get(url, headers=self.header)
        # 提取go方法中的参数
        # print(res2.text)
        data = json.loads(re.findall(r';go\((.*?)\)', res2.text)[0])
        jsl_clearance_s = self.getCookie(data)
        # 修改cookie
        add_dict_to_cookiejar(session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
        res3 = session.get(url, headers=self.header, verify=False)
        html = res3.text
        return html

    def main(self, url, origin_item):
        html = self.get_text(url)
        selector = Selector(text=html)
        item = {
            **origin_item,
        }
        for tr in selector.css(".zblist_table tr"):
            item['title_name'] = tr.css('td.zblist_xm a::text').get() or tr.css('td.td_left a::text').get()

            if item['title_name'] is None:
                continue
            title_url = tr.css('td.zblist_xm a::attr(href)').get() or tr.css('td.td_left a::attr(href)').get()
            if title_url is None:
                continue
            item['title_url'] = urljoin(url, title_url)
            item['title_date'] = tr.css('td:last-child::text').get()

            content_html = self.get_text(item['title_url'])
            selector = Selector(text=content_html)
            item['content_html'] = selector.css(".zhaobiaoxq").get()
            self.API.data_update(item)

    def run(self):

        orgin_item_list = [
            {
                "url_list": ["https://www.bidnews.cn/caigou/search-htm-page-{}-stype-fuwu.html".format(i) for i in
                             range(1, 10)],
                "site_path_url": "https://www.bidnews.cn/caigou/stype-fuwu.html",
                "site_path_name": "招标频道>服务",
                "site_id": "CBB2A7EE81",
                "site_name": "全国招标信息网-安徽",
                "title_type": "拟在建项目",
                "title_source": "全国招标信息网-安徽",
            },
            {
                "url_list": ["https://www.bidnews.cn/caigou/search-htm-page-{}-stype-gongcheng.html".format(i) for i in
                             range(1, 10)],
                "site_path_url": "https://www.bidnews.cn/caigou/stype-gongcheng.html",
                "site_path_name": "招标频道>工程",
                "site_id": "06720760BE",
                "site_name": "全国招标信息网-安徽",
                "title_type": "拟在建项目",
                "title_source": "全国招标信息网-安徽",
            },
            {
                "url_list": ["https://www.bidnews.cn/caigou/search-htm-page-{}-stype-huowu.html".format(i) for i in
                             range(1, 10)],
                "site_path_url": "https://www.bidnews.cn/caigou/stype-huowu.html",
                "site_path_name": "招标频道>货物",
                "site_id": "7ECFE5D99F",
                "site_name": "全国招标信息网-安徽",
                "title_type": "拟在建项目",
                "title_source": "全国招标信息网-安徽",
            },
            {
                "url_list":["https://www.bidnews.cn/ks/?page={}".format(i)for i in range(1,10)],
                "site_path_url": "https://www.bidnews.cn/ks/",
                "site_path_name": "招标频道>矿山",
                "site_id": "CF8A6AE122",
                "site_name": "全国招标信息网-安徽",
                "title_type": "拟在建项目",
                "title_source": "全国招标信息网-安徽",
            },
            {
                "url_list":["https://www.bidnews.cn/xiangmu/nizaijian-38070--{}.html".format(i)for i in range(1,10)],
                "site_path_url": "https://www.bidnews.cn/xiangmu/nizaijian-38070.html",
                "site_path_name": "项目频道>拟在建项目",
                "site_id": "F0A7BFCF10",
                "site_name": "全国招标信息网-安徽",
                "title_type": "拟在建项目",
                "title_source": "全国招标信息网-安徽",
            },
            {
                "url_list":["https://www.bidnews.cn/yj/?page={}".format(i)for i in range(1,10)],
                "site_path_url": "https://www.bidnews.cn/yj/",
                "site_path_name": "招标频道>冶金",
                "site_id": "B939363C75",
                "site_name": "全国招标信息网-安徽",
                "title_type": "拟在建项目",
                "title_source": "全国招标信息网-安徽",
            }

        ]

        for orgin_item in orgin_item_list:
            for url in orgin_item['url_list']:
                self.main(url, orgin_item)


if __name__ == '__main__':
    AnHuiWholeBidding().run()
