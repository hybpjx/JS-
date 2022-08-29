# -*- coding: utf-8 -*-
# @Time    : 2022/8/29 9:30
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : DaLianZhongGongProcurementManagenmentPlatform.py
# @Software: PyCharm
import re

import requests
from requests.utils import add_dict_to_cookiejar
from scrapy import Selector

from pkg.Invoking import APIInvoke


class DaLianZhongGongProcurementManagenmentPlatform:
    url = "http://eps.dhidcw.com/HomeSite/Site/Index"
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    API = APIInvoke()

    def get_cookie_session(self):
        res1 = self.session.get("http://eps.dhidcw.com/HomeSite/Site/Index", headers=self.headers)
        cookies = {}
        for k, v in res1.cookies.items():
            cookies[k] = v
        add_dict_to_cookiejar(self.session.cookies, cookies)

        html = res1.text

        return self.session, html

    def get_bidding_parse(self, click_url, site_item):
        session, html = self.get_cookie_session()
        selector = Selector(text=html)
        # 点击采购公告
        bidding_onclick = selector.css(
            '#blueIndex > div.container-fluid.navbar-bg > div.container > div > header > nav > ul > li:nth-child(2) > a').attrib[
            'onclick']
        bidding_url = "http://eps.dhidcw.com" + re.search(r"OpenPage\('(.*)',\d\)", bidding_onclick).group(1)
        html = session.get(bidding_url, headers=self.headers).text
        selector = Selector(text=html)

        # # 拿到询价公告的链接 / # 拿到中标公告的链接
        list_url = "http://eps.dhidcw.com" + selector.css(
            click_url).attrib['href']
        self.parse_write(list_url, session, site_item)

    def get_Winning_bid_parse(self, click_url, site_item):
        session, html = self.get_cookie_session()
        selector = Selector(text=html)
        # 点击中标公告
        bidding_onclick = selector.css(
            '#blueIndex > div.container-fluid.navbar-bg > div.container > div > header > nav > ul > li:nth-child(3) > a').attrib[
            'onclick']
        bidding_url = "http://eps.dhidcw.com" + re.search(r"OpenPage\('(.*)',\d\)", bidding_onclick).group(1)
        html = session.get(bidding_url, headers=self.headers).text
        selector = Selector(text=html)

        # 拿到询价招标公告的链接 / # 拿到询价中标公告的链接
        list_url = "http://eps.dhidcw.com" + selector.css(
            click_url).attrib['href']
        self.parse_write(list_url, session, site_item)

    def parse_write(self, list_url, session, site_item):
        html = session.get(list_url, headers=self.headers).text
        selector = Selector(text=html)
        item = {
            **site_item
        }
        for li in selector.css('.news-list.unlist li'):
            item['site_name'] = "大连重工电子采购平台"
            item['title_type'] = "拟在建项目"
            # 目标的标题
            item['title_name'] = li.css('a::attr(title)').get()
            # 目标详情页的地址
            item['title_url'] = 'http://eps.dhidcw.com/' + li.css('a::attr(href)').get()
            # 目标日期
            item['title_date'] = li.css('.date').re_first('20\d{2}-\d{2}-\d{2}')
            html = self.session.get(item['title_url'], headers=self.headers).text

            selector = Selector(text=html)

            item['content_html'] = selector.css("body").get()

            if item['content_html'] is None:
                item['content_html'] = """
                <div>
                详情页无内容
                </div>
                """
            self.API.data_update(item)

    def run(self):
        xjgg_url = "#form1 > div:nth-child(4) > div > div.col-lg-9.col-sm-9 > ul:nth-child(1) > li > a"
        xjgg_item = {
            "site_path_url": "http://eps.dhidcw.com/HomeSite/Site/Index",
            "site_path_name": "首页 /  询价公告",
            "site_id": "B66DEE497A",
        }
        self.get_bidding_parse(click_url=xjgg_url, site_item=xjgg_item)

        zb_url = "#form1 > div:nth-child(4) > div > div.col-lg-9.col-sm-9 > ul:nth-child(2) > li > a"
        zb_item = {
            "site_path_url": "http://eps.dhidcw.com/HomeSite/Site/Index",
            "site_path_name": "首页 /  招标公告",
            "site_id": "E3F26BDAB8",
        }
        self.get_bidding_parse(click_url=zb_url, site_item=zb_item)

        xjzbgg_url = "#form1 > div:nth-child(4) > div > div.col-lg-9.col-sm-9 > ul:nth-child(1) > li > a"
        xjzbgg_item = {
            "site_path_url": "http://eps.dhidcw.com/HomeSite/Site/Index",
            "site_path_name": "首页 / 询价中标公告",
            "site_id": "8635DD38A1",
        }
        self.get_bidding_parse(click_url=xjzbgg_url, site_item=xjzbgg_item)

        xjzb_url = "#form1 > div:nth-child(4) > div > div.col-lg-9.col-sm-9 > ul:nth-child(2) > li > a"
        xjzb_item = {
            "site_path_url": "http://eps.dhidcw.com/HomeSite/Site/Index",
            "site_path_name": "首页 / 招标中标公告",
            "site_id": "B00FCAB084",
        }
        self.get_bidding_parse(click_url=xjzb_url, site_item=xjzb_item)


if __name__ == '__main__':
    DaLianZhongGongProcurementManagenmentPlatform().run()
