# 精彩纵横
from typing import Any

import requests
from pyquery import PyQuery as pq
from lxml import etree
from tqdm import tqdm

from pkg.Invoking import APIInvoke


class Marvellousverticalhorizontal:
    session: Any = requests.session()
    proxies: dict = {
        # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
        'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
    }

    API: Any = APIInvoke()
    item: dict = {
        "site_path_url": 'http://www.jczh100.com/index/tendering/li.html?zhuanti=&et=&industry=&t=z&hangye=&so=&quyu=&gonggao=&xinxi=&page=2#somap',
        "site_path_name": "招标投标>精彩纵横公告",
        "site_id": "CBB86173EF",
        "site_name": "精彩纵横",
        "title_type": "拟在建项目",
        "title_source": "精彩纵横",
    }

    def parse(self):
        for url in tqdm([
                            f'http://www.jczh100.com/index/tendering/li.html?zhuanti=&et=&industry=&t=z&hangye=&so=&quyu=&gonggao=&xinxi=&page={i}#somap'
                            for i in range(1, 5)]):
            html = self.session.get(url, proxies=self.proxies).text
            for li in pq(html)(".pinfolist.pinfolist01 li").items():
                title_url = li("a").attr("href")
                if title_url is None:
                    continue
                self.item["title_url"] = "http://www.jczh100.com" + title_url
                self.item['title_name'] = li(".soGaoliang").text().replace(" ", "").replace("\n", "")
                self.item['title_date'] = str(li(".date.fl p.p2").text()).replace(" ", "").replace("\n", "")[5:]
                content_html = self.session.get(self.item['title_url'], proxies=self.proxies).text
                self.item['content_html'] = pq(content_html)(".box_l.fl")
                self.API.data_update(self.item)


if __name__ == '__main__':
    Marvellousverticalhorizontal().parse()
