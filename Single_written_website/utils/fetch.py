# -*- coding: utf-8 -*-
# @Time    : 2022/7/11 14:14
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : fetch.py
# @Software: PyCharm
from typing import Optional
import fake_useragent
import requests
from pkg.Invoking import APIInvoke
from utils.data_to_html import DataFormat
import json
import time as time_

from lxml import etree
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

class Fetch:
    def __init__(self):
        self.session = requests.session()
        self.df = DataFormat()
        self.API = APIInvoke()

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





class SeleniumSpider(WebDriver):
    """??????selenium???????????????"""

    def __init__(self, params=None, max_window=False, *args, **kwargs):
        """
        ?????????
        :param path: str selenium????????????
        :param params: list driver ????????????
        :param args: tuple
        :param kwargs:
        """
        self.__params = params
        # ?????????
        self.__options = Options()
        self.__options.add_argument('--dns-prefetch-disable')
        self.__options.add_argument('--disable-gpu')  # ???????????????????????????????????????????????????bug
        self.__options.add_argument('disable-infobars')  # ??????"Chrome?????????????????????????????????"
        # self.__options.add_argument('--headless')
        self.is_maximize_window = max_window  # ????????????????????????

        # ????????? ??????????????????: https://juejin.im/post/5c62b6d5f265da2dab17ae3c
        self.__options.add_experimental_option('excludeSwitches', ['enable-automation'])

        if params:
            for i in params:
                self.__options.add_argument(i)
        super(SeleniumSpider, self).__init__(options=self.__options, *args, **kwargs)
        # ?????????????????????
        self.execute_chrome_protocol_js(
            protocol="Page.addScriptToEvaluateOnNewDocument",
            params={"source": """
           Object.defineProperty(navigator, 'webdriver', {
           get: () => false,
           });"""})
        if self.is_maximize_window:
            self.maximize_window()

        # ????????????
        self.ID = "id"
        self.XPATH = "xpath"
        self.LINK_TEXT = "link text"
        self.PARTIAL_LINK_TEXT = "partial link text"
        self.NAME = "name"
        self.TAG_NAME = "tag name"
        self.CLASS_NAME = "class name"
        self.CSS_SELECTOR = "css selector"

    def cookies_dict_to_selenium_cookies(self, cookies: dict, domain):
        """
        requests cookies ????????? selenium cookies
        :param cookies: requests cookies
        :return: selenium ?????????cookies
        """
        temp_cookies = []
        for key, value in cookies.items():
            # requests ???bug ??????????????????????????? ???????????? ??????????????????????????????
            temp_cookies.append({"name": key, "value": value, "domain": domain})
        return temp_cookies

    def get(self, url: str, cookies=None, domain=None):
        """
        ????????????
        :param url: ????????????url
        :param cookies: ??????cookies cookies ?????? [{"name": key, "value": value, "domain": domain},...]
        :param domain: cookie?????????
        :return:
        """
        super().get(url)
        if cookies:
            # ??????
            if type(cookies) == list:
                for cookie in cookies:
                    if "name" in cookie.keys() and "value" in cookie.keys() and "domain" in cookie.keys():
                        self.add_cookie(cookie)
                    else:
                        raise TypeError('cookies???????????????????????????[{"name": key, "value": value, "domain": domain},...'
                                        '] ??????{key: vale,...}')
            elif type(cookies) == dict:
                if domain:
                    for i in self.cookies_dict_to_selenium_cookies(cookies, domain):
                        self.add_cookie(i)
                else:
                    raise ValueError("{key:vale}??????????????????doamin??????")
            # ????????????
            self.refresh()

    def web_driver_wait(self, time: int, rule: str, num: str):
        """
        ????????????  ?????????????????????????????? ?????????400??????
        :param time: ????????????
        :param rule: ?????? [id, xpath, link text, partial link text, name, tag name, class name, css selector]
        :param num: ????????????id
        :return:
        """
        WebDriverWait(self, time, 0.5).until(
            EC.presence_of_element_located((rule, num)))

    def web_driver_wait_ruishu(self, time: int, rule: str, num: str):
        """
        ????????? ??????????????????
        :param time: ????????????
        :param rule: ?????? [id, class]
        :param num: ????????????id
        :return:
        """
        while time:
            response = self.execute_js("document.documentElement.outerHTML")
            try:
                html = etree.HTML(text=response["value"])
                inp = html.xpath("//*[contains(@%s, '%s')]" % (rule, num))
                if inp:
                    break
            except Exception as e:
                continue
            time_.sleep(1)
            time -= 1
        if not time:
            raise Exception("????????? %s" % num)

    def execute_chrome_protocol_js(self, protocol, params: dict):
        """
        Chrome DevTools ???????????? ????????????????????? https://chromedevtools.github.io/devtools-protocol/
        :param protocol: str ????????????
        :param params: dict ??????
        :return:
        """
        resource = "/session/%s/chromium/send_command_and_get_result" % self.session_id
        command_executor = self.command_executor
        url = command_executor._url + resource
        body = json.dumps({'cmd': protocol, 'params': params})
        response = command_executor._request('POST', url, body)
        # print(response)
        # if response['status']:
        #     return response
        return response["value"]

    def execute_js(self, js):
        """
        ??????js  ???????????????
        :param js: str ????????????js
        :return:  {"type": "xxx", value: "xxx"}
        """
        resource = "/session/%s/chromium/send_command_and_get_result" % self.session_id
        command_executor = self.command_executor
        url = command_executor._url + resource
        body = json.dumps({'cmd': "Runtime.evaluate", 'params': {"expression": js}})
        response = command_executor._request('POST', url, body)
        # if response['status']:
        #     return response
        return response["value"]["result"]
