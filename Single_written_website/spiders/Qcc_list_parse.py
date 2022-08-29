# -*- coding: utf-8 -*-
# @Time    : 2022/8/11 10:29
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : Qcc_list_parse.py
# @Software: PyCharm
from urllib.parse import urljoin

import jsonpath
import requests
from pkg.Invoking import APIInvoke
from utils.fetch import Fetch


class QccListParse:

    def __init__(self):
        self.API = APIInvoke()
        self.Qcc_link = "https://www.qcc.com/firm/3900c2ed4f60b77bc7fdaeea24275539.html"

    def parse(self):
        import requests

        headers = {
            '98e03952ffd905286636': '0c7a26142e721873f36a20031ae89adc1ae4e965c1c1f097f9e932711600376f480f0587261f7515cfea4338722db1424f9b728c593a17a5fdff6730563de296',
            'cookie': 'qcc_did=7fcf57fe-6cc7-4543-8a13-afc52cb9d2b7; '
                      'UM_distinctid=18146294a0113eb-08d0ceae26f9eb-26021b51-1fa400-18146294a02115c; '
                      'zg_did=%7B%22did%22%3A%20%221814b2f03c8246-0812586db6e65c-26021b51-1fa400-1814b2f03c9110f%22%7D; '
                      'zg_5068e513cb8449879f83e2a7142b20a6=%7B%22sid%22%3A%201654823781325%2C%22updated%22%3A%201654823789620%2C%22info%22%3A%201654823781326%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E6%8B%9B%E6%8A%95%E6%A0%87WEB%E7%AB%AF%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%5C%22%24utm_source%5C%22%3A%20%5C%22baidu1%5C%22%2C%5C%22%24utm_medium%5C%22%3A%20%5C%22cpc%5C%22%2C%5C%22%24utm_term%5C%22%3A%20%5C%22pzsy_ztb%5C%22%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%7D; '
                      'QCCSESSID=5d9f03ecc6a46a6b536420f1e6; '
                      'acw_tc=b47a4e9c16601868773596459e5d342093ef7774b66f30c5ca6facc50c; '
                      'CNZZDATA1254842228=1217675831-1654737177-%7C1660185573',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            # 'x-pid': '24f101b7da495f915848785137648df8',
        }

        params = (
            ('keyNo', '3900c2ed4f60b77bc7fdaeea24275539'),
        )

        response = requests.get('https://www.qcc.com/api/datalist/tenderlist', headers=headers, params=params)

        return response.json()

    def main(self):
        json_data = self.parse()
        item = {}
        # print(json_data)
        for data in json_data['data']:
            print(data)
            item['site_path_url'] = self.Qcc_link
            item['site_path_name'] = jsonpath.jsonpath(json_data, "$..Name")[0]
            item['site_id'] = "293412180E"
            item['site_name'] = "企查查"
            item['title_type'] = "拟在建项目"
            item['title_source'] = "企查查"
            item['title_name'] = data['title']

            item['title_date'] = data['publishdate']

            title_url = data.get('originalurl', False)

            if title_url:
                item['title_url'] = title_url
                try:
                    item['content_html'] = Fetch().fetch_get(data['originalurl']).text
                except Exception:
                    item['content_html'] = data['content']
            else:
                item['title_url'] = urljoin(item['site_path_url'], item['title_name'])
                item['content_html'] = data['content']
            self.API.data_update(item)


if __name__ == '__main__':
    QccListParse().main()
