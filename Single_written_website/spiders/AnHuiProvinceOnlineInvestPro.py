# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 17:55
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : AnHuiProvinceOnlineInvestPro.py
# @Software: PyCharm
import re

import requests
from selenium import webdriver as uc

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke
from scrapy.selector import Selector


class AnHuiProvinceOnlineInvest:

    item = {'site_path_name': URL_DATA_INFO["AnHuiProvinceOnlineInvestPro"]["site_path_name"],
            'site_id': URL_DATA_INFO["AnHuiProvinceOnlineInvestPro"]["site_id"],
            'site_path_url': URL_DATA_INFO["AnHuiProvinceOnlineInvestPro"]["site_path_url"],
            'site_name': URL_DATA_INFO["AnHuiProvinceOnlineInvestPro"]["site_name"],
            'title_type': URL_DATA_INFO["AnHuiProvinceOnlineInvestPro"]["title_type"],
            'title_source': URL_DATA_INFO["AnHuiProvinceOnlineInvestPro"]["title_source"],
            }
    session = requests.session()
    url = "http://tzxm.ahzwfw.gov.cn/portalopenPublicInformation.do?method=queryExamineAll"
    API = APIInvoke()


    def get_cookie(self):
        js_source = """
var _0x5e8b26 = '3000176000856006061501533003690027800375'
var getAcwScV2 = function (arg1) {
    String['prototype']['hexXor'] = function (_0x4e08d8) {
        var _0x5a5d3b = '';
        for (var _0xe89588 = 0x0; _0xe89588 < this['length'] && _0xe89588 < _0x4e08d8['length']; _0xe89588 += 0x2) {
            var _0x401af1 = parseInt(this['slice'](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x105f59 = parseInt(_0x4e08d8['slice'](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x189e2c = (_0x401af1 ^ _0x105f59)['toString'](0x10);
            if (_0x189e2c['length'] == 0x1) {
                _0x189e2c = '0' + _0x189e2c;
            }
            _0x5a5d3b += _0x189e2c;
        }
        return _0x5a5d3b;
    };
    String['prototype']['unsbox'] = function () {
        var _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24];
        var _0x4da0dc = [];
        var _0x12605e = '';
        for (var _0x20a7bf = 0x0; _0x20a7bf < this['length']; _0x20a7bf++) {
            var _0x385ee3 = this[_0x20a7bf];
            for (var _0x217721 = 0x0; _0x217721 < _0x4b082b['length']; _0x217721++) {
                if (_0x4b082b[_0x217721] == _0x20a7bf + 0x1) {
                    _0x4da0dc[_0x217721] = _0x385ee3;
                }
            }
        }
        _0x12605e = _0x4da0dc['join']('');
        return _0x12605e;
    };
    var _0x23a392 = arg1['unsbox']();
    arg2 = _0x23a392['hexXor'](_0x5e8b26);
    return arg2
};
        """
        from execjs import compile

        html = self.session.get(self.url).text

        arg1 = re.search(r"var arg1='(.*)';", html).group(1)
        ctx = compile(js_source)
        acw_sc__v2 = ctx.call("getAcwScV2", arg1)
        return acw_sc__v2

    def main(self):
        # 获取cookie
        headers = {
            "Cookie": f"acw_sc__v2={self.get_cookie()};",
            'Host': 'tzxm.ahzwfw.gov.cn',
            'Origin': 'http://tzxm.ahzwfw.gov.cn',
            'Referer': 'http://tzxm.ahzwfw.gov.cn/portalopenPublicInformation.do?method=queryExamineAll',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

        }
        # 拿到主页面
        response = self.session.post(url=self.url, data={
            "pageSize": "20",
            "pageNo": "1",
            "apply_project_name": "",
            "projectInfo.areaDetialCode": "",
            "projectInfo.projectAddress": "",
            "projectInfo.areaDetial": "",
            "projectInfo.industryId": "",
            "projectInfo.industry": "",
        }, headers=headers, verify=False)
        # 使用scrapy 的selector对象解析 一定要指定 text 不然会报错
        selector = Selector(text=response.text)
        for tr in selector.css("#publicInformationForm tr"):
            onclick = tr.css("td a::attr(onclick)").get()
            # 正则匹配
            pattern = re.match("window\.open\(\'(.*?)\'\)", onclick)

            if pattern is None:
                continue

            self.item['title_url'] = "http://tzxm.ahzwfw.gov.cn/" + str(pattern.group(1))
            self.item['title_name'] = tr.css("td a::text").get()
            self.item['title_date'] = tr.css("td:nth-child(5)::text").get()
            # 拿到详情页的数据
            detail_response = self.session.get(self.item['title_url'], headers=headers)
            detail_selector = Selector(text=detail_response.text)
            self.item['content_html'] = detail_selector.css(".content_main").get()
            self.API.data_update(self.item)
        self.close_session()

    def close_session(self):
        self.session.close()


if __name__ == '__main__':
    AnHuiProvinceOnlineInvest().main()