# -*- coding: utf-8 -*-
# @Time    : 2022/7/11 14:14
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : fetch.py
# @Software: PyCharm
from typing import Optional
import fake_useragent
import requests
from pkg.Invoking import APIInvok
from pkg.utils.data_to_html import DataFormat


class Fetch:
    def __init__(self):
        self.session = requests.session()
        self.df = DataFormat()
        self.API = APIInvok()

    def fetch_get(self,
                  url,
                  headers: Optional = None,
                  proxies: Optional = None,
                  cookies: Optional = None):
        if headers:
            headers = headers
        else:
            headers = {
                "User-Agent": fake_useragent.UserAgent().random,
            }
        response = self.session.get(url=url, headers=headers, verify=False, timeout=(5, 15), proxies=proxies,
                                    cookies=cookies)
        response.encoding = response.apparent_encoding
        return response

    def fetch_post(self,
                   url,
                   headers: Optional = None,
                   proxies: Optional = None,
                   data: Optional = None,
                   json: Optional = None, ):
        if headers:
            headers = headers
        else:
            headers = {
                "User-Agent": fake_useragent.UserAgent().random,
            }

        if data:
            data = data

            response = self.session.post(url=url, headers=headers, verify=False, timeout=(5, 15), proxies=proxies,
                                         data=data)
            response.encoding = response.apparent_encoding
            return response
        if json:
            response = self.session.post(url=url, headers=headers, verify=False, timeout=(5, 15), proxies=proxies,
                                         json=json)
            response.encoding = response.apparent_encoding
            return response

        response = self.session.post(url=url, headers=headers, verify=False, timeout=(5, 15), proxies=proxies)
        response.encoding = response.apparent_encoding
        return response

    def close(self):
        self.session.close()


if __name__ == '__main__':
    Mixins().session()
