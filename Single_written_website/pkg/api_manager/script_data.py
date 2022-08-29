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
import time
import re
import datetime
import hashlib
import socket
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment

from .keywords import keywords_valid, keyword_ignore, keywords_search


class SpiderData(object):
    def __init__(self):
        pass

    def getApiIp(self):
        local_ip = ""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception as e:
            s.close()
        if "192.168.2" in local_ip:
            api_ip = "192.168.2.31"
        else:
            api_ip = "mykyls.xyz"
        print("local_ip:", local_ip, "API IP: ", api_ip)
        return api_ip

    def getSiteId(self, site_path_url):
        site_id = "-"
        try:
            site_path_url = site_path_url.strip()
            site_id = hashlib.md5(bytes(site_path_url, "utf-8")).hexdigest()[-10:].upper()
        except Exception as e:
            print("getSiteIdMap error:", str(e))
        return site_id

    def findValidKeyword(self, title_str):
        # 获取初选关键词
        keys_list = keywords_valid
        valid_keys = []
        for each_key in keys_list:
            if each_key in title_str:
                valid_keys.append(each_key)
        return valid_keys

    def findSearchKeyword(self, title_str):
        # 获取查询关键词
        keys_list = keywords_search
        valid_keys = []
        for each_key in keys_list:
            if each_key in title_str:
                valid_keys.append(each_key)
        keywords = []
        for each_keys in valid_keys:
            if each_keys in keywords:
                continue
            keywords.append(each_keys)
            
        cp_array = re.findall('[^\u4e00-\u9fa5]([\u4e00-\u9fa5（）]+?公司|集团)', title_str)
        cp_list = []
        for each_cp in cp_array:
            if len(each_cp) > 20:
                each_cp = each_cp[:20]
            if len(each_cp) > 3 and each_cp not in cp_list: 
                cp_list.append(each_cp)
        seach_str =  " ".join(keywords + cp_list)
        if len(seach_str) > 500:
            print(len(seach_str))
            return seach_str[:500]
        else:
            return seach_str

    def findPageTel(self, content):
        # 获取电话号码
        tel_array = re.findall('[^0-9](1[3456789]\\d{9}|0\\d{2}-\\d{8}|0\\d{3}-\\d{8}|0\\d{3}-\\d{7})[^0-9]', content)
        page_tel = ", ".join(tel_array)
        return page_tel

    @staticmethod
    def getTitleDate(page_str: str):
        """
        没有日的 自动变成每月的一号
        没有时间的 自动转换为当前时间
        超出当前时间30天的 自动转换为当前时间
        """
        # 获取日期
        # title_tag_str = "2021-06-03"
        # title_tag_str = "2021年06月03日"
        # title_tag_str = "2021/06/03"
        import datetime
        import re
        import time
        date_str = ""
        # 正则匹配如下
        re_str_list = [r"(20\d{2}[-年/.]\d+[-月/.]\d{2})",
                       r"(20\d{2}[-年/.]\d+[-月/.]\d{1})",
                       r"(20\d{2}-[01][0-9]--[0-3][0-9])",
                       r"(20\d{2}[-年/.]\d+[-月/.])",
                       ]

        # 遍历正则列表
        for re_str in re_str_list:
            temp_date_list = re.findall(re_str, page_str)
            # 如果匹配到
            if temp_date_list:
                # 直接赋值给 然后跳出循环
                date_str = temp_date_list[0]
                break

        #  如果匹配不到
        if date_str == "":
            # 然后再匹配
            re_str = "[^0-9]([0-3][0-9])(20\\d{2}-[01][0-9])"
            temp_date_list = re.findall(re_str, page_str)
            if temp_date_list:
                temp_list = list(temp_date_list[0])
                if len(temp_list) == 2:
                    date_str = "%s-%s" % (temp_list[1], temp_list[0])
        #  把年月日 -- / . 统统转换为-
        date_str = date_str.replace("年", "-").replace("月", "-").replace("日", "") \
            .replace("--", "-").replace("/", "-").replace(".", "-")
        temp_list = date_str.split("-")

        # 如果长度大于3
        if len(temp_list) == 3:
            # print(temp_list)
            # 如果第二个匹配项 例如 2022-1-1
            # 这个1 就要加个0
            if len(temp_list[1]) == 1:
                temp_list[1] = "0" + temp_list[1]
            # 同理
            if len(temp_list[2]) == 1:
                temp_list[2] = "0" + temp_list[2]

        date_str = "-".join(temp_list)
        # 获取当前时间
        now = datetime.datetime.now()
        # 在获取超过当前时间30天的时间
        delta = datetime.timedelta(days=3)
        n_days = now + delta
        # 格式化
        after_date = n_days.strftime('%Y-%m-%d')
        # 存在 且时间 在30天内 返回这个时间
        if date_str and date_str <= after_date:
            return date_str

    def checkTitleDate(self, title_date):
        try:
            n_ts = int(time.time()) + 3600 * 24 * 5
            ts = int(time.mktime(time.strptime(title_date, "%Y-%m-%d")))
            if n_ts - ts > 0:
                return True
            else:
                return False
        except Exception:
            return False

    def getHtmlData(self, html, page_url):
        html_data = {"file": [], "html": html, "text": ""}
        if not html:
            return {"file": [], "html": "", "text": ""}
        if "div" not in html:
            return html_data
        soup = BeautifulSoup(html, "lxml")
        [style.extract() for style in soup.findAll(text=lambda text: isinstance(text, Comment))]
        # if "<style" in html:
        [style.extract() for style in soup.findAll('style')]
        [style.extract() for style in soup.findAll('script')]
        [style.extract() for style in soup.findAll('meta')]
        [style.extract() for style in soup.findAll('link')]
        [style.extract() for style in soup.findAll('head')]
        [style.extract() for style in soup.findAll('header')]
        [style.extract() for style in soup.findAll('footer')]
        # [style.extract() for style in soup.findAll('iframe')]
        # for tag in soup.findAll(True):
        #     tag.attrs = None
        # 修改图片链接绝对链接
        html = str(soup)
        html = re.sub(r'\n{2,}', '\n', html)
        html = re.sub(r'&amp;', '&', html)
        #html = re.sub(r'class=".*"', "", html)
        file_url_array = []
        file_url_list = []  # 用于排除重复
        data_items_img = soup.select("img")
        for each_a in data_items_img:
            temp_url = each_a.get("src", "")
            file_url = self.getLinkUrl(page_url, temp_url)
            if "javascript" in temp_url or "()" in temp_url or temp_url.strip() == "":
                continue
            if temp_url != file_url:
                html = html.replace('"%s"' % temp_url, '"%s"' % file_url)
        # 提取附件
        data_items_file = soup.select("a")
        for each_a in data_items_file:
            temp_name = each_a.text.strip()
            temp_name_type = "None"
            if "." in temp_name:
                temp_name_type = temp_name.split(".")[-1].strip().lower()
            temp_url = each_a.get("href", "")
            temp_target = each_a.get("target", "None")
            temp_target_type = "None"
            if "." in temp_target:
                temp_target_type = temp_target.split(".")[-1].strip().lower()
            file_url = self.getLinkUrl(page_url, temp_url)
            if "javascript" in temp_url or "()" in temp_url or temp_url.strip() == "":
                continue
            if temp_url != file_url:
                html = html.replace(temp_url.strip(), file_url.strip())
            if temp_url:
                if file_url in file_url_list:
                    continue
                file_type_list = ["pdf", "doc", "docx", "xls", "xlsx", "zip", "rar",
                                  "tar.gz", "ppt", "txt", "png", "jpg"]
                url_file_name = temp_url.split(".")[-1].strip().lower()
                if temp_name_type in file_type_list or url_file_name in file_type_list:
                    file_url = self.getLinkUrl(page_url, temp_url)
                    if temp_url == file_url:
                        temp_url = ""
                    file_data = {"href": temp_url, "name": temp_name, "file_url": file_url}
                    file_url_array.append(file_data)
                    file_url_list.append(file_url)
                    continue
                elif temp_target_type in file_type_list:
                    file_url = self.getLinkUrl(page_url, temp_url)
                    if temp_url == file_url:
                        temp_url = ""
                    file_data = {"href": temp_url, "name": temp_target, "file_url": file_url}
                    file_url_array.append(file_data)
                    file_url_list.append(file_url)
                    continue
        html_data["text"] = re.sub(r'\n{2,}', '\n', soup.text)
        html_data["html"] = html
        html_data["file"] = file_url_array
        return html_data

    def getTitleID(self, temp_title_data):
        if temp_title_data["title_url"]:
            temp_str = temp_title_data["title_url"]
        else:
            temp_str = temp_title_data["site_name"] + "  " + temp_title_data["title_name"]
        title_id = hashlib.md5(temp_str.encode("utf-8")).hexdigest()
        return title_id

    def getLinkUrl(self, page_url, href):
        href = href.strip()
        if href.strip().startswith("http") or href == "N/A":
            page_url = href
        else:
            page_url = urljoin(page_url, href)
        return page_url

    def analysisTitleData(self, title_dict):
        title_data = {
            # -------search-------------------
            "title_id": title_dict.get("title_id", ""),
            "title_date": title_dict["title_date"],
            "title_name": title_dict["title_name"],
            "content_text": "",
            "site_id": "",
            "file_status": 1, # ((0, "附件错误"),(1, "已下载"),(2, "没有附件"),(3, "有附件"),)
            "importance": 0,  # ((0, "已排除"),(1, "已读"),(2, "未读"),(3, "已发布"),)
            "run_status": 1,  # ((0, "状态错误"),(1, "等待更新"),(2, "正在更新"),(3, "爬取结束"),)
            # "update_user": ""
            
            # -------detail------------------
            # "title_id": "",
            "update_time": str(datetime.datetime.now()),
            "update_user": title_dict.get("update_user"),
            "title_url": title_dict["title_url"],
            "site_name": title_dict["site_name"],
            "site_path_name": title_dict["site_path_name"],
            "site_path_url": title_dict["site_path_url"],
            "file_json": [],
            "keywords": [],
            "content_html": title_dict["content_html"],
        }
        title_data.update(title_dict)
        # check data
        if not title_data["title_id"]:
            title_data["title_id"] = self.getTitleID(title_dict)
        if not title_data["site_id"]:
            title_data["site_id"] = self.getSiteId(title_data["site_path_url"])
        if "http" in title_data["title_url"]:
            temp_url = title_data["title_url"]
        else:
            temp_url = title_dict["site_path_url"]
        html_data = self.getHtmlData(title_data["content_html"], temp_url)
        content_text = " ".join(html_data["text"].split())
        date_status = self.checkTitleDate(title_data["title_date"])
        if date_status is False:
            title_date = self.getTitleDate(content_text)
            date_status = self.checkTitleDate(title_date)
            if date_status is True:
                title_data["title_date"] = title_date
            else:
                title_data["title_date"] = datetime.datetime.now().strftime('%Y-%m-%d')
        title_data["content_html"] = html_data["html"]
        # title_data["tel"] = self.findPageTel(html_data["text"])
        # 附件状态
        title_data["file_json"] = html_data["file"]
        if title_data["file_json"]:
            title_data["file_status"] = 3
        else:
            title_data["file_status"] = 2
        # 关键词匹配
        seach_str = title_data["title_name"] + content_text
        title_data["keywords"] = self.findValidKeyword(seach_str)
        if title_data["keywords"]:
            title_data["importance"] = 2
            for each_key in keyword_ignore:
                if each_key in seach_str:
                    title_data["importance"] = 0
        else:
            title_data["importance"] = 1
        # 关键词查找
        title_data["content_text"] = self.findSearchKeyword(seach_str)
        if "运行错误" in title_data["content_html"]:
            title_data["run_status"] = 0
        elif title_data["content_html"] == "":
            title_data["run_status"] = 1
        else:
            title_data["run_status"] = 3
        return title_data

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
    tester = SpiderData()
    title_data = {
        "title_date": "2022-08-27",
        "title_name": "测试数据",
        "site_id": "123",
        "site_name": "测试数据",
        "title_type": "",
        "title_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/qtgg/zfj/10636259671725203456.html",
        "title_source": "",
        "site_path_name": "公告公示",
        "site_path_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/",
        "content_html": "<html><body><div>测试数据矿2022-01-27</div></body></html>",
        "update_user": "",
    }
    data = tester.analysisTitleData(title_data)    # 临时数据表
    # data = tester.checkTitleDate("2022-05-04")
    print(data)
