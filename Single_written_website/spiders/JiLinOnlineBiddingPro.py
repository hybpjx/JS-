# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 16:50
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : JiLinOnlineBiddingPro.py
# @Software: PyCharm
import re
import time
import datetime

import requests
import urllib3
import http.client
from lxml import etree
import http.client
from codecs import encode

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke
from utils.data_to_html import DataFormat

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class JiLinOnlineBidding:
    def __init__(self):
        self.item = {'site_path_name': URL_DATA_INFO["JiLinOnlineBiddingPro"]["site_path_name"],
                     'site_id': URL_DATA_INFO["JiLinOnlineBiddingPro"]["site_id"],
                     'site_path_url': URL_DATA_INFO["JiLinOnlineBiddingPro"]["site_path_url"],
                     'site_name': URL_DATA_INFO["JiLinOnlineBiddingPro"]["site_name"],
                     'title_type': URL_DATA_INFO["JiLinOnlineBiddingPro"]["title_type"],
                     'title_source': URL_DATA_INFO["JiLinOnlineBiddingPro"]["title_source"],
                     }
        self.proxy = {
            # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
            'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
        }

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        }

        self.session = requests.session()
        self.proxy = {
            # 'http':'http://通行证书:通行密钥@代理服务器的地址:代理地址的端口',
            'http': 'http://H29EUPO37A52DDLP:9AAFE3C1A393902A@http-pro.abuyun.com:9010',
        }
        self.df = DataFormat()
        self.API = APIInvoke()

    def get_text(self, url, data):
        response = self.session.post(url, data, headers=self.headers, verify=False, proxies=self.proxy)
        return response

    def parse(self):
        for i in range(1, 10):
            data = {
                "pageSize": "10",
                "pageNo": str(i),
                "apply_project_name": "",
            }
            response = self.get_text("https://tzxm.jl.gov.cn/portalopenPublicInformation.do?method=queryExamineAll",
                                     data=data)
            tree = etree.HTML(response.text)
            for tr in tree.xpath("//table[starts-with(@class,index-table)]//tr"):
                try:
                    title_name = tr.xpath('./td[1]/@title')[0]
                    title_name = str(title_name).replace("\n", "").replace(" ", "")
                except:
                    continue
                self.item['title_name'] = title_name
                self.item['title_url'] = title_name

                send_id = tr.xpath("./td[1]/a/@onclick")

                if not send_id:
                    continue
                else:
                    pattern = re.search('queryDetailed\(\'(.*?)\'\)', send_id[0])
                    if pattern is None:
                        break
                    else:
                        sendid = pattern.group(1)

                detail_data = {'sendid': sendid}
                detail_response = self.get_text(
                    url="https://tzxm.jl.gov.cn/portalopenPublicInformation.do?method=queryDetailed",
                    data=detail_data)

                data = detail_response.json()[0]

                self.item['title_date'] = data.get("real_finish_time", "")

                if self.item['title_date'] == "":
                    # 取年份
                    year_web = str(self.item['title_name'][-24:-22])
                    # 取月份
                    month_web = str(self.item['title_name'][-22:-20])
                    # 获取当前 年 月
                    today = datetime.datetime.today()
                    now_year = today.year
                    now_month = today.month
                    # 如果是这个月的 就默认今天
                    if year_web == now_year and month_web == now_month:
                        self.item['title_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        self.item['title_date'] = "20" + year_web + "-" + month_web + "-01"

                # json_dict = {
                #              "deal_code": data.get("deal_code",""),
                #             "apply_project_name": data.get("apply_project_name",""),
                #             "dept_name":data.get("dept_name",""),
                #             "legaperson_certno": data.get("legaperson_certno",""),
                #             "area_detial": data.get("area_detial",""),
                #             "cor_type_name": data.get("cor_type_name",""),
                #             "project_type": data.get("project_type",""),
                #             "total_money": data.get("total_money",""),
                #             "project_endtime": data.get("project_endtime",""),
                #             "project_starttime": data.get("project_starttime",""),
                #             "obtainresult": data.get("obtainresult",""),
                #             "approval_num": data.get("approval_num",""),
                #             "deal_dept_name": data.get("deal_dept_name",""),
                #             "real_finish_time": data.get("real_finish_time",""),
                #             "industry_name": data.get("industry_name",""),
                #             "scale_content": data.get("scale_content",""),
                #              }

                content_html = f"""
                <table>
<tbody>
<tr>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd ;"><strong>项目编码</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd ;">{data.get("deal_code", "")}</td>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;"> <strong>项目名称</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;"> {data.get("apply_project_name", "")}</td>
</tr>
<tr>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd ;"><strong>单位名称</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd ;">{data.get("dept_name", "")}</td>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;"> <strong>社会统一信用代码</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;"> {data.get("legaperson_certno", "")}</td>
</tr>
<tr>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd ;"><strong>建设地点</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd ;">{data.get("area_detial", "")}</td>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;"> <strong>项目单位申报类型</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;"> {data.get("cor_type_name", "")}</td>
</tr>
<tr>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd ;"><strong>建设性质</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd ;">{data.get("project_type", "")}</td>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;"> <strong>项目总投资（万元）</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;"> {data.get("total_money", "")}</td>
</tr>

<tr>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd ;"><strong>计划竣工时间</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd ;">{data.get("project_endtime", "")}</td>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;"> <strong>计划开工时间</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;"> {data.get("project_starttime", "")}</td>
</tr>

<tr>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd ;"><strong>审核结果</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd ;">{data.get("obtainresult", "")}</td>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;"> <strong>备案流水号</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;"> {data.get("approval_num", "")}</td>
</tr>

<tr>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd ;"><strong>备案机关</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd ;">{data.get("deal_dept_name", "")}</td>
<td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;"> <strong>备案日期</strong></td>
<td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">{data.get("real_finish_time", "")}</td>
</tr>

<tr><td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;" colspan="1"><strong>项目所属行业</strong></td>
        <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd;" colspan="3"> {data.get("industry_name", "")}</td></tr>
<tr><td style="width: 150px; color: black; padding: 6px 10px; border: solid 1px #ddd;" colspan="1"><strong>主要建设规模及内容</strong></td>
        <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd;" colspan="3">{data.get("scale_content", "")}</td></tr>
</tbody>
</table>
                
                """

                self.item['content_html'] = content_html

                self.API.data_update(self.item)
        self.session.close()

    def close_session(self):
        self.session.close()


if __name__ == '__main__':
    JiLinOnlineBidding().parse()
