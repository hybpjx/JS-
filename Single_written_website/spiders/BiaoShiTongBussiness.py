import json
import re

from pyquery import PyQuery as pq
import requests
import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from browsermobproxy import Server
from selenium.webdriver.common.by import By

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke


class BiaoShiTongBussiness:
    server = Server(r'D:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()

    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    # 添加特殊配置
    # 设置默认编码为utf-8，也就是中文
    options.add_argument('lang=zh_CN.UTF-8')
    # 模拟androidQQ浏览器
    # options.add_argument(
    #     'user-agent="MQQBrowser/26Mozilla/5.0(Linux;U;Android2.3.7;zh-cn;MB200Build/GRJ22;CyanogenMod-7)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1"')
    # 禁止硬件加速
    options.add_argument('--disable-gpu')
    # 取消沙盒模式
    options.add_argument('--no-sandbox')
    # 禁止弹窗广告
    options.add_argument('--disable-popup-blocking')
    # 最大界面
    options.add_argument('--window-size=1920,1080')
    # 去掉反扒标志
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 此方法针对V78版本及以上有效，同时可以解决部分网站白屏的问题。
    options.add_experimental_option('useAutomationExtension', False)
    ##大量渲染时候写入/tmp而非/dev/shm
    options.add_argument("-–disable-dev-shm-usage")
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"
    # 忽略证书错误（实操没卵用）
    options.add_argument('--ignore-certificate-errors')
    proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })

    def get_data(self):
        self.driver.get("http://www.biaoshitong.com/search/project")
        self.driver.find_element(By.CSS_SELECTOR, ".last-page.turn-page.page-btn").click()
        time.sleep(1)
        result = self.proxy.har
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            if "querySearchList" in _url:
                _response = entry['response']
                _content = _response['content']['text']
                print(
                    "------https://www.biaoshitong.com/biaoshitong/business-server/xinxiguanli/querySearchList 请求响应内容：",
                    _content)
                # print(str(_content).replace("'", "\""))
                dic_str = json.loads(str(_content).replace("'", "\""))
                for data in dic_str['data']['rows']:
                    item = {}
                    item['title_name'] = data['ggName']
                    # print(data)
                    if item == "":
                        continue
                    item['title_date'] = data['fabuTime']
                    item['title_url'] = data['href']
                    if item['title_url'] is None:
                        continue
                    try:
                        html = requests.get(item['title_url']).text

                        item['content_html'] = pq(html)("body").html()

                        if item['content_html'] is None:
                            item['content_html'] = "请查看原文链接"
                    except:
                        item['content_html'] = "请查看原文链接"

                    item['site_path_name'] = URL_DATA_INFO["BiaoShiTongBussiness"]["site_path_name"]
                    item['site_id'] = URL_DATA_INFO["BiaoShiTongBussiness"]["site_id"]
                    item['site_path_url'] = URL_DATA_INFO["BiaoShiTongBussiness"]["site_path_url"]

                    item['site_name'] = URL_DATA_INFO["BiaoShiTongBussiness"]["site_name"]
                    item['title_type'] = URL_DATA_INFO["BiaoShiTongBussiness"]["title_type"]
                    item['title_source'] = URL_DATA_INFO["BiaoShiTongBussiness"]["title_source"]
                    API = APIInvoke()
                    API.data_update(item)
        self.driver.find_element(By.CSS_SELECTOR, ".last-page.turn-page.page-btn").click()
        self.close()

    def close(self):
        self.server.stop()
        self.driver.close()


if __name__ == '__main__':
    BiaoShiTongBussiness().get_data()
