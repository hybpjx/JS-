import random
import requests
from pyquery import PyQuery as pq

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke
from utils.Mixins import Mixins

is_update: bool = True
cnf = APIInvoke(is_update=is_update)


class AnHuiProvincePlatformPro:
    proxy_list = []

    def get_proxy(self):
        import requests
        response = requests.get(
            "http://dec.ip3366.net/api/?key=20220622092726414&getnum=30&anonymoustype=3&filter=1&area=1&order=2&sarea=1&formats=2")

        if response.status_code == 200:
            for data in response.json():
                ip = data['Ip']
                port = data['Port']
                proxy_ip = str(ip) + ":" + str(port)

                self.proxy_list.append(proxy_ip)

                return random.choice(self.proxy_list)

        else:
            print("代理ip链接已过期")

    def fetch(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            # "cookie": "Hm_lvt_2bfb8d2d4303cc91d8f06fa464f36346=1647828607; Hm_lvt_e2329777c4106c325d471eec6259333f=1647847747,1648518393,1648633433,1648690033; wzws_cid=80595d6867c2199207f5c28cb3eaa17210b283094d6d5bc9e0a87fa1af5131afec12cc837d6e8944caa98fb07d8cc26472c63064241ccc7997bb077cfa15d26c0cdc463359d0d854daf38cf76b5f2df3; X-LB=1.0.19.dc23260b; JSESSIONID=C110D88B4743B55BBB2EB8E5E912DAF5"
        }
        proxy = {
            # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
            'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
        }

        response = requests.get(url, headers=headers, proxies=proxy)
        return response

    def get_data(self, url, meta):

        # proxy_ip = self.get_proxy()
        # print(proxy_ip)
        # proxies = {
        #     'http': 'http://' + proxy_ip,
        #     'https': 'https://' + proxy_ip
        # }

        html = self.fetch(url).text

        doc = pq(html)

        item = {}
        for li in doc("div.list.clear > ul:nth-child(2) > li.list-item").items():
            title_url: str = li('a').attr('href')

            item["site_path_url"] = meta['site_path_url']
            item["site_path_name"] = meta['site_path_name']
            item["site_id"] = meta['site_id']
            item['title_name'] = li('.title.clamp-1').text()
            item['title_url'] = Mixins().Get_domain_name(url=meta['site_path_url'], title_url=title_url)
            item['title_date'] = li.css('.date.float-r.m-r-40').text()
            detail_html = self.fetch(item['title_url']).text
            detail_doc = pq(detail_html)
            item['content_html'] = detail_doc(".tran-info-detail-content.float-l").html()
            item['site_name'] = URL_DATA_INFO["AnHuiProvicePlatformPro"]["site_name"]
            item['title_type'] = URL_DATA_INFO["AnHuiProvicePlatformPro"]["title_type"]
            item['title_source'] = URL_DATA_INFO["AnHuiProvicePlatformPro"]["title_source"]
            cnf.data_update(item)

    def run(self):
        meta_list = [
            {
                "site_path_url": "http://ggzy.ah.gov.cn/jsgc/list?tenderProjectType=A01",
                "site_path_name": "交易信息>政府采购",
                "site_id": "D4E9809AE1",
            },
            {
                "site_path_url": "http://ggzy.ah.gov.cn/kyqcr/list",
                "site_path_name": "土地矿权首页>交易信息>土地矿权",
                "site_id": "57338DA792",
            },
            {
                "site_path_url": "http://ggzy.ah.gov.cn/zfcg/list",
                "site_path_name": "首页>审批信息",
                "site_id": "3D1298258E",
            },

        ]

        for meta in meta_list:
            self.get_data(url=meta['site_path_url'], meta=meta)


if __name__ == '__main__':
    AnHuiProvincePlatformPro().run()
