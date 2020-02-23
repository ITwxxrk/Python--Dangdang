# -*- coding: utf-8 -*-

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


import scrapy
from dangdang.items import DangdangItem
from scrapy.http import Request # 依次爬取的工具

class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pgl-cid4008154.html']
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64:x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',}

    def parse(self, response):
        item = DangdangItem()
        item["title"] = response.xpath('//p[@name="title"]/a/@title').extract()
        item["link"] = response.xpath('//p[@name="title"]/a/@href').extract()
        item["comment"] = response.xpath('//a[@dd_name="单品评论"]/text()').extract()
        item["shop"] = response.xpath('//p/a[@dd_name="单品店铺"]/text()').extract()
        item["price"] = response.xpath('//span[@class="price_n"]/text()').extract()
        print(item)
        yield item # 将数据提交到Pipeline中
        for i in range(2,2001):
            url = 'http://category.dangdang.com/pg'+str(i)+'-cid4008154.html'
            # callback为回调函数
            yield Request(url,callback=self.parse,headers=self.header)



