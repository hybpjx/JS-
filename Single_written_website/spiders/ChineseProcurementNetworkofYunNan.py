import time

from autoselenium import Driver
from lxml import etree
from selenium.webdriver.common.by import By

from conf.diff_config import URL_DATA_INFO
from pkg.Invoking import APIInvoke


class YunNanCaiGouSpider:
    API = APIInvoke()
    item = {
        "site_name": URL_DATA_INFO["ChineseProcurementNetworkofYunNan"]["site_name"],
        "site_path_url": URL_DATA_INFO["ChineseProcurementNetworkofYunNan"]["site_path_url"],
        "site_path_name": URL_DATA_INFO["ChineseProcurementNetworkofYunNan"]["site_path_name"],
        "title_type": URL_DATA_INFO["ChineseProcurementNetworkofYunNan"]["title_type"],
        "site_id": URL_DATA_INFO["ChineseProcurementNetworkofYunNan"]["site_id"],
        "title_source": URL_DATA_INFO["ChineseProcurementNetworkofYunNan"]["title_source"],
    }

    def main(self):
        with Driver('chrome', root='drivers') as driver:
            driver.get(self.item['site_path_url'])
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            # write_to_html(driver.page_source)
            html = etree.HTML(driver.page_source)
            trs = html.xpath("//table[@id='bulletinlistid']//tr")[1:]
            for tr in trs:
                try:
                    self.item["title_name"] = tr.xpath("./td/a/text()")[0]
                except IndexError:
                    print("验证失败")
                    break
                self.item["title_date"] = tr.xpath("./td[4]/text()")
                driver.find_element(By.XPATH,
                                         f'//table[@id="bulletinlistid"]//td/a[contains(text(), "{self.item["title_name"]}")]').click()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)
                self.item["title_url"] = driver.current_url
                self.item["content_html"] = etree.tostring(
                    etree.HTML(driver.page_source).xpath("//*[@class='panel-body']")[0])
                self.API.data_update(self.item)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        


if __name__ == '__main__':
    YunNanCaiGouSpider().main()
