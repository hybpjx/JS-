# -*- coding: utf-8 -*-
# @Time    : 2022/7/12 11:17
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : ShangHaiBaoWubiddingBussiness.py
# @Software: PyCharm
import time
from conf.diff_config import URL_DATA_INFO
from utils import fetch


class ShangHaiBaoWubiddingBussiness:
    def __init__(self):
        self.fm = fetch.Fetch()

        self.item = {'site_path_name': URL_DATA_INFO["ShangHaiBaoWubiddingBussiness"]["site_path_name"],
                     'site_id': URL_DATA_INFO["ShangHaiBaoWubiddingBussiness"]["site_id"],
                     'site_path_url': URL_DATA_INFO["ShangHaiBaoWubiddingBussiness"]["site_path_url"],
                     'site_name': URL_DATA_INFO["ShangHaiBaoWubiddingBussiness"]["site_name"],
                     'title_type': URL_DATA_INFO["ShangHaiBaoWubiddingBussiness"]["title_type"],
                     'title_source': URL_DATA_INFO["ShangHaiBaoWubiddingBussiness"]["title_source"],
                     }

    def main(self):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'csrfToken=do8ekMBgjjhoNUEToUuwjN7b;',
            'Host': 'qiye.obei.com.cn',
            'Referer': 'https://qiye.obei.com.cn/web-zone/bwzy/procurement.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-csrf-token': 'do8ekMBgjjhoNUEToUuwjN7b'
        }

        url = "https://qiye.obei.com.cn/web-zone/api/sys/zone/getPurchaseList"

        for page_num in range(1, 10):
            payload = {"code": "bwzy",
                       "noticeType": "1",
                       "pageNum": page_num,
                       "pageSize": 10,
                       "pageFlag": "addSelect",
                       "sidx": "issueDate",
                       "sord": "desc"}

            self.info_get(headers, payload, url)
        #
        url = "https://qiye.obei.com.cn/web-zone/api/sys/zone/getMakeList"
        for page_num in range(1, 5):
            payload = {"code": "bwzy",
                       "noticeType": "2",
                       "pageNum": page_num,
                       "pageSize": 10,
                       "pageFlag": "addSelect",
                       "sidx": "requestEndDate",
                       "sord": "desc"}

            self.info_get(headers, payload, url)

        self.fm.close()

    def info_get(self, headers, payload, url):
        response = self.fm.fetch_post(url, headers=headers, json=payload, proxies={
            # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
            'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
        })
        for data in response.json()['data']:
            print(data)
            self.item['title_name'] = data['title']
            self.item['title_date'] = data.get('issueDate')
            if self.item['title_date'] is None:
                self.item['title_date'] = data.get('requestEndDate')
                if self.item['title_date'] is None:
                    self.item['title_date'] = time.strftime('%Y-%m-%d %H:%M:%S')

            self.item[
                'title_url'] = f"https://qiye.obei.com.cn/web-zone/bwzy/procurementDetail.html?id={data['id']}&rfqMethod={data['rfqMethod']}&type=1"

            detail_payload = {"id": data['id'],
                              "rfqMethod": data['rfqMethod'],
                              "status": "1",
                              "page": "1",
                              "rows": 9999}

            response = self.fm.fetch_post(url="https://qiye.obei.com.cn/web-zone/api/sys/zone/getNoticeDetail",
                                          json=detail_payload, headers=headers, proxies={
                    # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
                    'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
                })
            json_text = response.json()

            data = json_text['data']['requestDto']
            ouRfqNum = data.get("ouRfqNum", "")
            publicBiddingFlag = data.get("publicBiddingFlag", "")
            linkmanName = data.get("linkmanName", "")
            linkmanTelphone = data.get("linkmanTelphone", "")
            registrationEndDate = data.get("registrationEndDate", "")

            if registrationEndDate != "":
                registrationEndDate = str(registrationEndDate).split("T")[0]

            quotationEndDate = data.get("quotationEndDate", "")
            if quotationEndDate != "":
                quotationEndDate = str(quotationEndDate).split("T")[0]

            deliveryAddress = data.get("deliveryAddress", "")
            assureMoney = data.get("assureMoney", "")
            requestBusiTerms = data.get("requestBusiTerms", "")
            requestTecTerms = data.get("requestTecTerms", "")

            content_html_1 = f"""
    
    
                           <tr><td style="400px: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd; background-color: #8AEC57FF">询价单号</td>
                                <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; background-color: #8AEC57FF" colspan="8">{ouRfqNum}</td></tr>
                    <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">采购方式</td>
                                <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="8">{publicBiddingFlag}</td></tr>
                    <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">联系人</td>
                                <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="8">{linkmanName}</td></tr>
                    <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">联系电话</td>
                                <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="8">{linkmanTelphone}</td></tr>
                    <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">报名截至时间</td>
                                <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="8">{registrationEndDate}</td></tr>
                    <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">报价截至时间</td>
                                <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="8">{quotationEndDate}</td></tr>
    
    
    
    
    
    
                    <tr><td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;" colspan="16">
                    <p>
                       一、交货地址: <span> {deliveryAddress}</span>
                    </p>
    
                    <p>
                      二、保证金额度: <span>{assureMoney} 元</span>
                    </p>
    
                    <p>
                     三、商务条款<br>
                      {requestBusiTerms}
                    </p>
    
                    <p>
                       四、技术条款<br>
                        {requestTecTerms}
                    </p>
    
                         </tbody></table>     
    
                            """

            requestItemList = json_text['data']['requestItemList']

            content_html_2 = ""
            for index, data in enumerate(requestItemList):
                materialNo = data.get("materialNo", "")
                materialName = data.get("materialName", "")
                characters = data.get("characters", "")
                producer = data.get("producer", "")
                requestAmount = data.get("requestAmount", "")
                unit = data.get("unit", "")
                requestDeliveryDate = data.get("requestDeliveryDate", "")

                if requestDeliveryDate != "":
                    requestDeliveryDate = str(requestDeliveryDate).split("T")[0]

                memo = data.get("memo", "")

                content_html_2 += f"""
                    <table>
                    <tbody>
    
                        <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd; background-color: #9DD2FCFF ">物料代码</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; background-color: #9DD2FCFF " colspan="16">{materialNo}</td>
                        </tr>
                        <tr>
                        <td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">物料名称</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="16">{materialName}</td>
                                    </tr>
                        <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">规格型号</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="16" >{characters}</td>
                                    </tr>
                        <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">品牌</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="16">{producer}</td>
                                    </tr>
                        <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">采购数量</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="16">{requestAmount}</td>
                                    </tr>
                        <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">计量单位</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="16">{unit}</td>
                                    </tr>
                        <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">要求交货期</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="16">{requestDeliveryDate}</td>
                                    </tr>
                        <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">备注</td>
                                    <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; " colspan="16">{memo}</td>
                                    </tr>
    
                              <tr><td style="width: 400px; color: #666; padding: 6px 10px; border: solid 1px #ddd; text-align: center " colspan="16">  </td></tr>
                                """
            self.item['content_html'] = content_html_2 + content_html_1

            self.fm.API.data_update(self.item)


if __name__ == '__main__':
    ShangHaiBaoWubiddingBussiness().main()
