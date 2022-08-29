#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
====================================================================
Project Name: mining spider
File description:
Author: Liao Heng
Create Date: 2021-08-22
====================================================================
"""


class DataFormat(object):
    def __init__(self):
        pass

    def dictToHtml(self, data_dict={}, name_dict={}):
        # 将字典数据转页面格式显示
        # return: html string
        str_list = ["<table>"]
        for each_key in data_dict:
            name = name_dict.get(each_key, each_key)
            temp_str = '''<tr><td style="width: 150px; color: #666; padding: 6px 10px; border: solid 1px #ddd;">%s</td>
            <td style="width: 800px; color: #666; padding: 6px 10px; border: solid 1px #ddd; ">%s</td></tr>''' % \
                       (name, data_dict[each_key])
            str_list.append(temp_str)
        str_list.append("</table>")
        return "\n".join(str_list)


if __name__ == "__main__":
    tester = DataFormat()
    data_dict = {
        "title_date": "2021-09-17",
        "title_name": "测试数据",
        "site_name": "测试数据",
        "title_type": "",
        "title_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/qtgg/zfj/10636259671725203456.html",
        "title_source": "",
        "site_path_name": "公告公示",
        "site_path_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/",
        "content_html": "测试数据项目共建16栋住宅楼、部分底商240.57m²，地下建筑面积为77405.55m²。",
        "update_user": "",
    }
    name_dict = {
        "title_date": "发布日期",
        "title_name": "标题名称",
        "site_name": "网站名称",
        "title_type": "信息类型",
        "title_url": "原文链接",
        "title_source": "数据来源",
        "site_path_name": "目录",
        "site_path_url": "目录地址",
        "content_html": "内容描述",
        "update_user": "更新用户",
    }
    content_html = tester.dictToHtml(data_dict, name_dict)
    print(content_html)
