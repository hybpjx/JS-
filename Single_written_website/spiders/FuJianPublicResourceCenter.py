# -*- coding: utf-8 -*-
# @Time    : 2022/7/13 16:39
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : FuJianPublicResourceCenter.py
# @Software: PyCharm
import base64
import datetime
import hashlib
import json
import time
import requests
from Cryptodome.Cipher import AES

# https://ggzyfw.fujian.gov.cn/web/index.html#/business/list?timeType=6&KIND=GCJS&PROTYPE=&BeginTime=2021-10-27%2000%3A00%3A00&EndTime=2022-04-27%2023%3A59%3A59
from pkg.Invoking import APIInvoke
from conf.diff_config import URL_DATA_INFO


class FuJianPublicResourceCenter:
    URL_DATA_INFO_TYPE = "FuJianPublicResourceCenter"
    URL_DATA_INFO_URL = 0
    item = {
        'site_path_name': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_path_name'][URL_DATA_INFO_URL],
        'site_id': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_id'][URL_DATA_INFO_URL],
        'site_path_url': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_path_url'][URL_DATA_INFO_URL],
        'site_name': URL_DATA_INFO[URL_DATA_INFO_TYPE]['site_name'],
        'title_type': URL_DATA_INFO[URL_DATA_INFO_TYPE]['title_type'],
        'title_source': URL_DATA_INFO[URL_DATA_INFO_TYPE]['title_source'],
    }
    session = requests.session()

    list_url = 'https://ggzyfw.fujian.gov.cn/Trade/TradeInfo'

    detail_post_url = "https://ggzyfw.fujian.gov.cn/Trade/TradeInfoContent"

    API = APIInvoke()

    secret_key = 'BE45D593014E4A4EB4449737660876CE'[0:32]  # 密钥

    iv = "A8909931867B0425"[0:16]  # 初始向量

    # 需要补位，str不是16的倍数那就补足为16的倍数
    def add_to_16(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)

    # 解密方法
    def aes_decrypt(self, key, t, iv):
        aes = AES.new(self.add_to_16(key), AES.MODE_CBC, self.add_to_16(iv))  # 初始化加密器
        base64_decrypted = base64.decodebytes(t.encode(encoding='utf-8'))  # 优先逆向解密 base64 成 bytes
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')  # 执行解密密并转码返回str
        return decrypted_text

    def less_data(self, less_data):
        now = datetime.datetime.now()
        # 在获取超过当前时间30天的时间
        delta = datetime.timedelta(days=less_data)
        n_days = now - delta
        return str(n_days).split(' ')[0]

    def get_sign_data(self, sign):
        # md5 加密
        portal_sign = hashlib.md5(sign.encode(encoding='utf-8')).hexdigest()

        return portal_sign

    def timestamp(self, shijian):
        s_t = time.strptime(shijian, "%Y-%m-%d %H:%M:%S")
        mkt = int(time.mktime(s_t))
        return mkt

    def parse(self):
        padding = lambda detail_decrypted_str: detail_decrypted_str[:detail_decrypted_str.rfind("}") + 1]

        for url in range(1, 6):
            ts = int(time.time() * 1000)
            # 封装请求体
            js_data = {"pageNo": url, "pageSize": 20, "total": 5679, "AREACODE": "", "M_PROJECT_TYPE": "",
                       "KIND": "GCJS",
                       "GGTYPE": "1", "PROTYPE": "", "timeType": "6", "BeginTime": f"{self.less_data(180)} 00:00:00",
                       "EndTime": f"{self.less_data(0)} 23:59:59", "createTime": [], "ts": ts}
            # 伪装sign
            sign = f'3637CB36B2E54A72A7002978D0506CDFBeginTime{js_data["BeginTime"]}createTime[]EndTime{js_data["EndTime"]}GGTYPE{js_data["GGTYPE"]}KIND{js_data["KIND"]}pageNo{js_data["pageNo"]}pageSize{js_data["pageSize"]}timeType{js_data["timeType"]}total{js_data["total"]}ts{js_data["ts"]}'
            # 执行公用的方法  返回值是未经过加密的 数据
            encrypted_str = self.encrypted_str_get(self.list_url, js_data, sign)
            # 执行AES解密的方法 把 key 和IV 传入
            decrypted_str = self.aes_decrypt(self.secret_key, encrypted_str, self.iv)
            js_text = json.loads(padding(decrypted_str))
            for data in js_text['Table']:
                self.item['title_name'] = data['NAME'].replace("<br>", "")
                self.item['title_date'] = data.get('TM')
                self.item[
                    'title_url'] = f"https://ggzyfw.fujian.gov.cn/web/index.html#/business/detail?cid={data['M_ID']}&type={data['KIND']}"
                if self.item['title_date'] is None:
                    self.item['title_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                # 封装请求体
                # 1657709230
                # 执行js代码
                payload = {"m_id": data['M_ID'], "type": data['GGTYPE'], "ts": int(time.time() * 1000)}
                # 伪装详情页的sign sign = "3637CB36B2E54A72A7002978D0506CDFm_id216262ts1657708358505type1"
                detail_sign = f"3637CB36B2E54A72A7002978D0506CDFm_id{payload['m_id']}ts{payload['ts']}type{payload['type']}"
                # 执行公用的方法  返回值是未经过加密的 数据
                encrypted_str = self.encrypted_str_get(self.detail_post_url, payload, detail_sign)
                # 执行AES解密的方法 把 key 和IV 传入
                detail_decrypted_str = self.aes_decrypt(self.secret_key, encrypted_str, self.iv)
                content_html = json.loads(padding(detail_decrypted_str))
                self.item['content_html'] = content_html.get("Contents", "")
                self.API.data_update(self.item)
        self.close()

    def encrypted_str_get(self, url, js_data, sign):
        portal_sign = self.get_sign_data(sign)
        headers = {
            'portal-sign': portal_sign,
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.0.0 Safari/537.36',
        }

        proxies = {
            # # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
            'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
        }

        response = self.session.post(url, headers=headers, json=js_data, proxies=proxies)

        encrypted_str = response.json()

        return encrypted_str['Data']

    def close(self):
        self.session.close()


if __name__ == '__main__':
    fjpr = FuJianPublicResourceCenter()
    fjpr.parse()
