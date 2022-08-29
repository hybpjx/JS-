import requests
import ddddocr

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke
from settings.log_conf import logger
from pyquery import PyQuery as pq

is_update: bool = True
cnf = APIInvoke(is_update=is_update)


class WholeInvestPro:
    API = APIInvoke(is_update=is_update)

    ocr = ddddocr.DdddOcr()

    yzm_url = "http://new.tzxm.gov.cn/website-service/servlet/validateCodeServlet"

    session = requests.session()

    post_url = "http://new.tzxm.gov.cn/website-service/announce/search"

    def parse(self, NODE_CODE):
        image_obj = self.session.get(self.yzm_url).content

        with open("../code/code.jpg", 'wb')as fp:
            fp.write(image_obj)
        with open('../code/code.jpg', 'rb') as f:
            img_bytes = f.read()

        res = self.ocr.classification(img_bytes)
        logger.info(f"此次访问的验证码为：{res}")
        data = {
            "code": str(res),
            "PAGE_NO": 1,
            "NODE_CODE": NODE_CODE,
            "PROJECT_CODE": "",
            "ITEM_CODE": "",
            "DEPT_CODE": "",
            "CURRENT_STATE": "全部",
            "RECEIVED_DATE": "",
            "COMPLETED_DATE": "",
        }
        json_data = self.session.post(self.post_url, data=data).json()

        item = {}
        try:
            js_data = json_data['DATA']
        except KeyError:
            print("本次验证码验证失败")
            return

        for json in js_data:
            item["title_name"] = json["PROJECT_NAME"]
            PROJECTUUID = json["PROJECTUUID"]
            ITEM_ID = json["ITEM_ID"]
            item[
                "title_url"] = f"http://new.tzxm.gov.cn/qita/xmbljggsxq/index.shtml?PROJECTUUID={PROJECTUUID}&ITEM_ID={ITEM_ID}"
            item["title_date"] = json["REAL_FINISH_TIME"]

            html = self.session.get(item['title_url']).text

            doc = pq(html)

            item['content_html'] = doc(".jggs_topbg").html()
            # 调用
            item['site_path_name'] = URL_DATA_INFO["WholeInvestPro"]["site_path_name"]
            item['site_id'] = URL_DATA_INFO["WholeInvestPro"]["site_id"]
            item['site_path_url'] = URL_DATA_INFO["WholeInvestPro"]["site_path_url"]
            item['site_name'] = URL_DATA_INFO["WholeInvestPro"]["site_name"]
            item['title_type'] = URL_DATA_INFO["WholeInvestPro"]["title_type"]
            item['title_source'] = URL_DATA_INFO["WholeInvestPro"]["title_source"]
            self.API.data_update(item)

    def run(self):
        self.parse("地方项目")
        self.parse("全国项目")


if __name__ == '__main__':
    WholeInvestPro().run()
