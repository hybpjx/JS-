# https://stbdfile.stdzzb.com/bdfileservice/sealpdf/M6100000992000369001/002208/undefined/fe407e3e2f404066bab84b33da8aac9c.pdf

import http.client
from codecs import encode
import gzip
import pyquery
from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke


class ShaanXiElectronicBiddingPro:
    API = APIInvoke()

    conn = http.client.HTTPSConnection("stbid.stdzzb.com")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=typ;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("1"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=kbyxq_time;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("2022-07-01 09:30:00"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=ggyxq_time;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("2022-06-16 17:00:00"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=pageNumber;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("1"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=pageSize;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("20"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=sortColumns;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("undefined"))
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))

    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '1452',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'stbid.stdzzb.com',
        'Origin': 'https://stbid.stdzzb.com',
        'Referer': 'https://stbid.stdzzb.com/exp/sigc/zbysggPage.do?typ=1',
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }

    def main(self):
        self.conn.request("POST", "/exp/sigc/zbysggPage.do", self.payload, self.headers)
        res = self.conn.getresponse()
        data = res.read()

        html = gzip.decompress(data).decode("utf-8")

        doc = pyquery.PyQuery(html)

        list_query = doc(".stzb_notlist li").items()

        item = {}

        for li in list_query:
            item['title_name'] = li("dl dt a").text()
            title_date = li("dl dd label").text()
            item['title_date'] = str(title_date)[5:15]
            print(item)
            View_url = li("dl dt a").attr("href")[19:39]

            item['title_url'] = f"https://stbid.stdzzb.com/exp/bidding/sell/signup/toZbggInfo.do?probid={View_url}"

            item['content_html'] = "PDF 文件"

            item['site_path_name'] = URL_DATA_INFO["ShaanXiElectronicBiddingPro"]["site_path_name"]
            item['site_id'] = URL_DATA_INFO["ShaanXiElectronicBiddingPro"]["site_id"]
            item['site_path_url'] = URL_DATA_INFO["ShaanXiElectronicBiddingPro"]["site_path_url"]

            item['site_name'] = URL_DATA_INFO["ShaanXiElectronicBiddingPro"]["site_name"]
            item['title_type'] = URL_DATA_INFO["ShaanXiElectronicBiddingPro"]["title_type"]
            item['title_source'] = URL_DATA_INFO["ShaanXiElectronicBiddingPro"]["title_source"]
            #
            self.API.data_update(item)


if __name__ == '__main__':
    seb=ShaanXiElectronicBiddingPro()
    seb.main()