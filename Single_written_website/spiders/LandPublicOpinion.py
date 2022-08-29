# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 13:18
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : LandPublicOpinion.py
# @Software: PyCharm
import fake_useragent
import requests
from requests.utils import add_dict_to_cookiejar
from scrapy import Selector
from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke


class LandPublicOpinion:
    headers = {"User-Agent": fake_useragent.UserAgent().random}

    item = {'site_path_name': URL_DATA_INFO["LandPublicOpinion"]["site_path_name"],
            'site_id': URL_DATA_INFO["LandPublicOpinion"]["site_id"],
            'site_path_url': URL_DATA_INFO["LandPublicOpinion"]["site_path_url"],
            'site_name': URL_DATA_INFO["LandPublicOpinion"]["site_name"],
            'title_type': URL_DATA_INFO["LandPublicOpinion"]["title_type"],
            'title_source': URL_DATA_INFO["LandPublicOpinion"]["title_source"],
            }
    API = APIInvoke()
    session = requests.session()

    def gain_cookies(self):
        response = self.session.get('http://www.tdyq.org.cn/list-tzgg.html', headers=self.headers, verify=False)

        security_session_verify = response.cookies.values()[0]
        add_dict_to_cookiejar(self.session.cookies, {'security_session_verify': security_session_verify})

        response2 = self.session.get(
            "http://www.tdyq.org.cn/list-tzgg.html?security_verify_data=313932302c31303830",
            headers=self.headers, verify=True
        )

        security_session_mid_verify = response2.cookies.values()[0]
        add_dict_to_cookiejar(self.session.cookies, {'security_session_mid_verify': security_session_mid_verify})
        return self.session

    def main(self):
        self.session = self.gain_cookies()
        resp = self.session.get(url=self.item['site_path_url'])
        selector = Selector(text=resp.text, type='html')
        for li in selector.css('#bigguotu li.haha'):
            self.item["title_url"] = li.css('a::attr(href)').get()
            self.item["title_date"] = li.css('span::text').get()
            self.item["title_name"] = li.css('a::attr(title)').get()
            respond = self.session.get(url=self.item["title_url"])
            content = Selector(text=respond.text, type='html')
            self.item["content_html"] = content.css('#content-con_left-content').get()

            self.API.data_update(self.item)

        self.session.close()


if __name__ == '__main__':
    LandPublicOpinion().main()
