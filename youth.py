# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from lxml import etree
import time
from pool import RandomPool
import json
from urllib.parse import urljoin
from db import DB
import random


class YouthSpider:

    def __init__(self):
        pool = RandomPool()
        ua = pool.get_user_agent()
        proxy = pool.get_ip()
        opts = FirefoxOptions()
        # 无界面选项
        opts.add_argument("--headless")
        # ubuntu上大多没有gpu，所以–disable-gpu以免报错
        opts.add_argument('--disable-gpu')
        # user-agent
        opts.add_argument('--user-agent=%s' % ua)
        # proxy
        opts.add_argument('--proxy-server=https://%s' % proxy)
        self.start_url = "http://news.youth.cn/gn/"
        self.browser = webdriver.Firefox(options=opts)
        self.db = DB()

    def parse_url(self, url):
        self.browser.get(url)
        return self.browser.page_source

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        li_list = html.xpath("//div[@class='rdwz']/ul[@class='tj3_1']/li")
        content_list = []
        for li in li_list:
            item = {}
            item["title"] = li.xpath("./a/text()")
            item["title"] = item["title"][0].strip()
            item["href"] = li.xpath("./a/@href")
            item["href"] = item["href"][0].strip()
            item["publish_time"] = li.xpath("./font/text()")
            item["publish_time"] = item["publish_time"][0].strip()
            print(item)
            content_list.append(item)

        # 下一页
        next_url_list = html.xpath("//a[contains(text(),'下一页')]/@href")
        next_url = next_url_list[0] if next_url_list else None
        return content_list, next_url

    def save_to_file(self, content_list):
        file_path = "中国青年网.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                f.write("\n")

    def save_to_db(self, content_list):
        for content in content_list:
            self.db.save_to_mongo(content)

    # 实现主要逻辑
    def run(self):
        # 1.start_url
        url = self.start_url
        while url:
            time.sleep(random.uniform(3,5))
            url = urljoin(self.start_url, url)
            # 2.发送请求，获取响应
            html_str = self.parse_url(url)
            # 3.提取数据，提取下一页元素
            content_list, url = self.get_content_list(html_str)
            # 4.保存数据
            self.save_to_file(content_list)
            self.save_to_db(content_list)


if __name__ == '__main__':
    youth_spider = YouthSpider()
    youth_spider.run()
