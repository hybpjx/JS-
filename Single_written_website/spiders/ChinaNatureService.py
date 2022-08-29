# # -*- coding: utf-8 -*-
# # @Time    : 2022/7/29 15:12
# # @Author  : lzc
# # @Email   : hybpjx@163.com
# # @File    : ChinaNatureService.py
# # @Software: PyCharm
# import re
# import time
# from scrapy.selector import Selector
# # from playwright import
#
# from pkg.Invoking import APIInvoke
# from utils.data_to_html import DataFormat
#
# import xmltodict, json
#
#
# class ChinaNatureService:
#     name_dict = {
#         "naMineName": "项目名称",
#         "approvalDate": "批准日期",
#         "province": "省份",
#         "qtLatStart": "起始纬度",
#         "qtLatEnd": "终止纬度",
#         "qtLonStart": "起始经度",
#         "qtLonEnd": "终止经度",
#         "naApplyPerson": "公司",
#         "qtArea": "面积",
#         "businessType": "项目类型",
#         'naGeographyPosition': '地理位置',
#         'approvalStatus': '受理状态',
#         'qtMainMine': '开采矿种',
#         'naMineKind': '矿权',
#         'naMineKindName': '矿权名称'
#     }
#
#     key = re.compile(r'</(.*?)>', re.S)
#     value = re.compile(r'>(.*?)<', re.S)
#     API = APIInvoke
#
#     driver = uc.Chrome()
#
#     def parse_kyqysl(self, url_list, item):
#         for url in url_list:
#             dumps_json = self.get_json(url)
#
#             for data in dumps_json['ResponseObj']['repMap']['list']:
#                 item['title_name'] = data['projectName']
#                 item[
#                     'title_url'] = f'https://zwfw.mnr.gov.cn:8090/tlwserver/publicservices/bjgs/kq/yq_ck?id={data["id"]}'
#                 item['title_date'] = data['approvalDate']
#                 try:
#                     detail_json = self.get_json(item['title_url'])
#                     item['content_html'] = DataFormat().dictToHtml(detail_json['CkYqGsEntity'], self.name_dict)
#                 except TypeError:
#                     item['content_html'] = DataFormat().dictToHtml(data, self.name_dict)
#                 self.API().data_update(item)
#
#     def parse_bjgsKflyFags(self, url_list, item):
#         for url in url_list:
#             dumps_json = self.get_json(url)
#             for data in dumps_json['ResponseObj']['repMap']['plgsInfoEntityList']:
#                 item['title_name'] = data['fagsQdmcTitle']
#                 item[
#                     'title_url'] = f'https://zwfw.mnr.gov.cn:8090/bjgsKflyFagsDetail?fagsId={data["id"]}'
#                 item['title_date'] = data['fagsKssj']
#                 try:
#                     detail_json = self.get_json(item['title_url'])
#                     item['content_html'] = DataFormat().dictToHtml(detail_json['repMap'], self.name_dict)
#                 except TypeError:
#                     item['content_html'] = DataFormat().dictToHtml(data, self.name_dict)
#                 self.API().data_update(item)
#
#     def parse_kyqypz(self, url_list, item):
#         for url in url_list:
#             dumps_json = self.get_json(url)
#
#             for data in dumps_json['ResponseObj']['repMap']['list']:
#                 item['title_name'] = data['projectName']
#                 item[
#                     'title_url'] = f'https://zwfw.mnr.gov.cn:8090/tlwserver/publicservices/bjgs/kq/yq_ck?id={data["id"]}'
#                 item['title_date'] = data['approvalDate']
#                 try:
#                     detail_json = self.get_json(item['title_url'])
#                     item['content_html'] = DataFormat().dictToHtml(detail_json['CkYqGsEntity'], self.name_dict)
#                 except TypeError:
#                     item['content_html'] = DataFormat().dictToHtml(data, self.name_dict)
#                 self.API().data_update(item)
#
#     def get_json(self, url):
#         self.driver.get(url=url)
#         content_html = self.driver.page_source
#         selector = Selector(text=content_html, type='html')
#         html = selector.css('pre::text').get()
#         o = xmltodict.parse(html)
#         dumps_json = json.loads(json.dumps(o))
#         return dumps_json
#
#     def run(self):
#         self.parse_kyqysl(
#             url_list=[
#                 'https://zwfw.mnr.gov.cn:8090/tlwserver/publicservices/bjgs/main?type=kyq&projectName=&licenseKey=&businessType=&obligee=&approvalDate=&approvalState=%E5%B7%B2%E5%8F%97%E7%90%86&' \
#                 f'pageNum={num}&pageSize=10' for num in range(1, 2)],
#             item={
#                 "site_name": "自然资源部政务服务门户",
#                 "title_type": "国家部委",
#                 "site_path_url": "https://zwfw.mnr.gov.cn/flow/open?type=kyqysl",
#                 "site_path_name": "矿业权登记受理信息公开",
#                 "title_source": "自然资源部政务服务门户",
#                 "site_id": "D29C4CA128",
#             },
#         )
#
#         time.sleep(1)
#
#         self.parse_bjgsKflyFags(
#             url_list=[
#                 f'https://zwfw.mnr.gov.cn:8090/tlwserver/publicservices/bjgs/fags/initKflyFags?approvalDate=&pageNum={num}&pageSize=10&timestamp=1660544155664'
#                 for num in range(1, 2)],
#             item={
#                 "site_name": "自然资源部政务服务门户",
#                 "site_path_url": 'https://zwfw.mnr.gov.cn:8090/bjgsKflyFags',
#                 "site_path_name": "矿产资源开发利用方案",
#                 "title_type": "国家部委",
#                 "site_id": "08CE9E9B6D",
#                 "title_source": "自然资源部政务服务门户",
#             },
#         )
#         time.sleep(1)
#         self.parse_kyqypz(
#             url_list=[
#                 f'https://zwfw.mnr.gov.cn:8090/tlwserver/publicservices/bjgs/main?type=ckdyba&projectName=&licenseKey=&businessType=&obligee=&approvalDate=&approvalState=&pageNum={num}&pageSize=10&timestamp=1660542992028'
#                 for num in range(1, 2)],
#             item={
#                 "site_name": "自然资源部政务服务门户",
#                 "site_path_url": 'https://zwfw.mnr.gov.cn:8090/bjgs?type=kyqypz',
#                 "site_path_name": "矿业权登记办理结果公开",
#                 "title_type": "国家部委",
#                 "site_id": "66331CB7FF",
#                 "title_source": "自然资源部政务服务门户",
#             },
#         )
#         time.sleep(1)
#         #  暂时没的搞
#         self.parse_kyqypz(
#             url_list=[
#                 f'https://zwfw.mnr.gov.cn:8090/tlwserver/publicservices/bjgs/main?type=ckdyba&projectName=&licenseKey=&businessType=&obligee=&approvalDate=&approvalState=&pageNum={num}&pageSize=10&timestamp=1661147296701'
#                 for num in range(1, 2)],
#             item={
#                 "site_name": "自然资源部政务服务门户",
#                 "site_path_url": 'https://zwfw.mnr.gov.cn:8090/bjgs?type=ckdyba',
#                 "site_path_name": "矿业权抵押备案",
#                 "title_type": "国家部委",
#                 "site_id": "AA664FB952",
#                 "title_source": "自然资源部政务服务门户",
#             },
#         )
#
#         self.spider.close()
#
#
# if __name__ == '__main__':
#     ChinaNatureService().run()
