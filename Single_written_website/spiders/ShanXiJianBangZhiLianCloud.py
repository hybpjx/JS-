# -*- coding: utf-8 -*-
import json
import re
from concurrent.futures import ThreadPoolExecutor
import js2py
import requests

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke
from utils.data_to_html import DataFormat


class ShanXiJianBangZhiLianCloud:
    API = APIInvoke()
    df = DataFormat()

    def execjs_run(self):

        js_text = '''
        var data = Math.random().toString(36).substr(2)

        '''
        content = js2py.EvalJs()
        content.execute(js_text)
        back_ = "_jsonp"
        return content.data + back_

    # 询价公告
    def main(self):

        with requests.Session() as session:
            params = {
                "searchName": "",
                "type": "pp",
                "bidType": "purchase",
                "supEnterpriseIds": "37953",
                "status": "0",
                "pageSize": "10",
                "pageIndex": "0",
                "innercode": "",
                "callback": self.execjs_run()
            }

            html, item = self.get_data(params, session)

            for data in html['result']:
                item['site_path_name'] = "首页->成交公告"
                item['site_id'] = "40D3C42BEF"

                self.parse(data, item)

    # 招标公告
    def main2(self):
        with requests.Session() as session:
            params = {
                "searchName": "",
                "type": "pp",
                "bidType": "purchase",
                "supEnterpriseIds": "37953",
                "status": "4",
                "pageSize": "10",
                "pageIndex": "0",
                "innercode": "",
                "callback": self.execjs_run()
            }
            html, item = self.get_data(params, session)

            for data in html['result']:
                item['site_path_name'] = "首页->招标公告;首页->询价公告"
                item['site_id'] = "9147108805"

                self.parse(data, item)

    # 成交公告
    def main3(self):
        with requests.Session() as session:
            params = {
                "searchName": "",
                "type": "pp",
                "bidType": "purchase",
                "supEnterpriseIds": "37953",
                "status": "10",
                "pageSize": "10",
                "pageIndex": "0",
                "innercode": "",
                "callback": self.execjs_run()
            }
            html, item = self.get_data(params, session)

            for data in html['result']:
                item['site_path_name'] = "首页->招标公告;首页->询价公告"
                item['site_id'] = "9147108805"

                self.parse(data, item)

    def parse(self, data, item):
        item['title_name'] = data['messageTitle']
        item['title_date'] = data['entryTime']
        item[
            'title_url'] = f"https://yc.yonyoucloud.com/cpu-fe-tender/dist/inquirydetail/index.html?id={data['msgId']}"
        item['content_html'] = self.df.dictToHtml(data)
        item['site_path_url'] = URL_DATA_INFO["ShanXiJianBangZhiLianCloud"]["site_path_url"]
        item['site_name'] = URL_DATA_INFO["ShanXiJianBangZhiLianCloud"]["site_name"]
        item['title_type'] = URL_DATA_INFO["ShanXiJianBangZhiLianCloud"]["title_type"]
        item['title_source'] = URL_DATA_INFO["ShanXiJianBangZhiLianCloud"]["title_source"]
        self.API.data_update(item)

    def get_data(self, params, session):
        response = session.get("https://yc.yonyoucloud.com/yuncai/jsonp/supplierOffer/list", params=params)
        response.encoding = response.apparent_encoding
        html = response.text
        json_text = re.search(r"\((\[.*?\])\)", html).group(1)
        html = json.loads(json_text)[0]
        item = {}
        return html, item

    def run(self):
        self.main()
        self.main2()
        self.main3()

    def queue_run(self):
        # 通过多线程 来请求 队列中的数据 # 每秒请求几个 就 写几个 workers
        pool = ThreadPoolExecutor(max_workers=100)

        pool.submit(self.run)


if __name__ == '__main__':
    ShanXiJianBangZhiLianCloud().queue_run()
