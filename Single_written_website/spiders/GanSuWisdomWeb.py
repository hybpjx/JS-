# -*- coding: utf-8 -*-
# @Time    : 2022/6/27 10:11
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : GanSuWisdomWeb.py
# @Software: PyCharm


import requests
from lxml import etree

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke
from utils.data_to_html import DataFormat


class GanSuWisdomWeb:
    def __init__(self):
        self.item = {'site_path_name': URL_DATA_INFO["GanSuWisdomWeb"]["site_path_name"],
                     'site_id': URL_DATA_INFO["GanSuWisdomWeb"]["site_id"],
                     'site_path_url': URL_DATA_INFO["GanSuWisdomWeb"]["site_path_url"],
                     'site_name': URL_DATA_INFO["GanSuWisdomWeb"]["site_name"],
                     'title_type': URL_DATA_INFO["GanSuWisdomWeb"]["title_type"],
                     'title_source': URL_DATA_INFO["GanSuWisdomWeb"]["title_source"],
                     }
        self.url = "http://www.zhygcg.com/webpage/web/allarticleInfo.jsp?title=%25E7%259F%25BF&type=0"
        self.post_url = "http://www.zhygcg.com/a/website/annogoodstype/getAnnoByDate"
        self.form_data = {'platCode': '0',
                          'serachKey': '矿'}
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '30',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'jeeplus.session.id=c66e469e68f04b999bf3410d5b23cd95; Hm_lvt_3c822d6e0a6b59c58ccecfaef37b1cda=1656294093; JSESSIONID=7DAE08518DF2FBF55A0B2BE873F167A8; Hm_lpvt_3c822d6e0a6b59c58ccecfaef37b1cda=1656294106; jeeplus.session.id=65c2bfffe8984be58a306f4a81b8da63',
            'Host': 'www.zhygcg.com',
            'Origin': 'http://www.zhygcg.com',
            'Referer': 'http://www.zhygcg.com/webpage/web/allarticleInfo.jsp?title=%25E7%259F%25BF&type=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session = requests.session()
        self.df = DataFormat()
        self.API = APIInvoke(False)

    def main(self):
        proxy = {
            # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
            'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
        }
        response = self.session.post(url=self.post_url, headers=self.headers, data=self.form_data, proxies=proxy)
        for data in response.json():
            self.item['title_name'] = data['title']
            self.item[
                'title_url'] = f"http://www.zhygcg.com/a/website/annogoodstype/getAnnoDetailById?index=1&id={data['id']}&annoType={data['annoType']}"

            self.item['title_date'] = data['publicTime']

            html = self.session.get(self.item['title_url']).text

            tree = etree.HTML(html)

            content_html = tree.xpath("//div[starts-with(@class,detailsText)]")[0]

            self.item['content_html'] = etree.tostring(content_html, encoding='utf-8', method='html').decode('utf-8')

            self.API.data_update(self.item)

        self.close()

    def close(self):
        self.session.close()


if __name__ == '__main__':
    GanSuWisdomWeb().main()
