import time
import fake_useragent
from scrapy.selector import Selector
from requests.cookies import RequestsCookieJar
from selenium import webdriver as s
from selenium.webdriver import DesiredCapabilities
from seleniumwire import webdriver as sw, webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


def driver_set(wd):
    options = wd.ChromeOptions()
    # options.add_argument("--headless")  # 隐藏浏览器
    options.add_argument('--disable-gpu')  # 禁用GPU加速
    options.add_argument('--incognito')  # 隐身模式（无痕模式）
    options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--ignore-certificate-errors')  # https驱动
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'--user-agent={fake_useragent.UserAgent().random}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = wd.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
    })
    return driver


class SeleniumSpider(object):
    """
    SeleniumSpider工具类
        模仿浏览器访问获取加载完毕的源码数据
        __init__:初始化selenium启动浏览器并设置检测规避
        request_get:用selenium发送get请求
        requests_cookies:获取requests库可使用的cookies
        selector:标签选择器
        close:关闭浏览器
    """

    def __init__(self, wd='s'):
        if wd == 's':
            self.driver = driver_set(s)
        elif wd == 'uc':
            self.driver = uc.Chrome(use_subprocess=True)
        self.driver.maximize_window()

    def request_get(self, url, stop_time=0, load_time=6):
        """
        浏览器模拟发送get请求
        超时自动终止(最长6秒)
        :param url: url链接
        :param stop_time: 等待时长的开启(True)与关闭(False)默认关闭
        :param load_time: 加载最长时长6秒超出自动中断默认开启
        :return: 无返回值直接调用driver即可
        """
        if load_time:
            self.driver.set_page_load_timeout(load_time)
        try:
            self.driver.get(url=url)
            if stop_time:
                time.sleep(stop_time)
        except Exception:
            self.driver.execute_script('window.stop()')

    def requests_cookies(self, url, on_of=True):
        # 获取cookies并输出为requests的cookies格式直接使用
        selenium_cookies = self.driver.get_cookies()
        requests_cookies = RequestsCookieJar()
        for item in selenium_cookies:
            requests_cookies.set(item["name"], item["value"])
        return requests_cookies

    def selector(self):
        """
        标签选择器
        :return:返回一个selector对象
        """
        return Selector(text=self.driver.page_source, type='html')

    def into_iframe(self, path):
        """
        进入iframe
        path:为iframe的css标签位置
        """
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, path))

    def close(self):
        self.driver.close()


class SeleniumWireSpider(object):
    """
    基于SeleniumWire的工具类:
    用于获取请求头和响应头信息
     __init__:初始化SeleniumWire启动浏览器并设置检测规避
    request_get:用selenium发送get请求
    get_request_headers:获取请求头headers详细信息
    get_response_headers:获取响应头headers详细信息
    close:关闭浏览器
    """

    def __init__(self):
        self.driver = driver_set(wd=sw)
        self.driver.maximize_window()

    def request_get(self, url, stop_time=(int, False), load_time=True):
        """
        浏览器模拟发送get请求
        超时自动终止(最长6秒)
        :param url: url链接
        :param stop_time: 等待时长的开启(True)与关闭(False)默认关闭
        :param load_time: 加载最长时长6秒超出自动中断默认开启
        :param selector: 标签选择器
        :return: 无返回值直接调用driver即可
        """
        if load_time:
            self.driver.set_page_load_timeout(6)
        try:
            self.driver.get(url=url)
            if stop_time[1]:
                time.sleep(stop_time[0])
        except Exception:
            self.driver.execute_script('window.stop()')

    def get_request_headers(self, key: str):
        """
        获取请求头headers详细信息
        :return返回对应请求头元素list
        """
        request_list = list()
        # print(self.driver.requests)
        for request in self.driver.requests:
            if request.headers[key]:
                request_list.append(request.headers[key])
        if request_list:
            return request_list
        else:
            print('key列表为空')

    def get_response_headers(self, key: str):
        """
        获取响应头headers详细信息
        :return返回对应响应头元素list
        """
        response_list = list()
        print(self.driver.requests)
        for request in self.driver.requests:
            if request.response.headers[key]:
                response_list.append(request.response.headers[key])
        return response_list

    def selector(self):
        """
        标签选择器
        :return:返回一个selector对象
        """
        return Selector(text=self.driver.page_source, type='html')

    def into_iframe(self, path):
        """
        进入iframe
        path:为iframe的css标签位置
        """
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, path))

    def close(self):
        """
        关闭浏览器
        """
        self.driver.close()


class ImitateUcClass:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.driver = None

    def setOptions(self):
        # 设置默认编码为utf-8，也就是中文
        self.options.add_argument('lang=zh_CN.UTF-8')
        # 模拟androidQQ浏览器
        self.options.add_argument(
            'user-agent="MQQBrowser/26Mozilla/5.0(Linux;U;Android2.3.7;zh-cn;MB200Build/GRJ22;CyanogenMod-7)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1"')
        # 禁止硬件加速
        self.options.add_argument('--disable-gpu')
        # 取消沙盒模式
        self.options.add_argument('--no-sandbox')
        # 禁止弹窗广告
        self.options.add_argument('--disable-popup-blocking')
        # 最大界面
        self.options.add_argument('--window-size=1920,1080')
        # 去掉反扒标志
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 此方法针对V78版本及以上有效，同时可以解决部分网站白屏的问题。
        self.options.add_experimental_option('useAutomationExtension', False)
        # 大量渲染时候写入/tmp而非/dev/shm
        self.options.add_argument("-–disable-dev-shm-usage")
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
        # 忽略证书错误（实操没卵用）
        self.options.add_argument('--ignore-certificate-errors')
        return self.options

    def chrome(self, executable_path=""):
        if executable_path == "":
            self.driver = webdriver.Chrome(options=self.options)
        else:
            self.driver = webdriver.Chrome(executable_path=r"D:\Anaconda3\chromedriver.exe", options=self.options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        return self.driver

    def getDriver(self):
        self.setOptions()
        return self.chrome()


if __name__ == '__main__':
    # url = 'http://www.cmre-jh.com/Page/Web_ZB.aspx?oid=23'
    spider = SeleniumSpider()
    spider.request_get(
        url='http://www.ewkzb.com/index/portal/project_pro_info.htm?id=E110100WKZB220775001&bidSummary=1&pubId=51316CD1462B6048D6737E5DBFCDCB79',
        stop_time=3, load_time=False)
    print(spider.driver.page_source)
    # hand = spider.driver.window_handles  # 获取当前的所有句柄
    # print(hand)  # 打印当前的所有句柄
    # spider.driver.switch_to_window(hand[1])  # 转换窗口至最高的句柄
    # # spider.driver.switch_to(hand[-1])
    # # spider.driver.switch_to()
    # spider.into_iframe('.adz_guanbi iframe')
    # print(spider.driver.page_source)
    # spider.driver.switch_to.frame(spider.driver.find_element_by_css_selector('#conTarget'))
    # spider.driver.switch_to.frame(spider.driver.find_element(By.CSS_SELECTOR, '#conTarget'))
    # spider.into_iframe('#conTarget')
    # print(spider.selector().css('div.right_contents').getall())
