__author__ = 'kaneki'

import re
import scrapy
from scrapy.selector import Selector
from appstore.items import AppstoreItem

class HuaweiSpider(scrapy.Spider):
    name = "huawei"
    allowed_domains = ["huawei.com"]

    start_urls = [
        "http://appstore.huawei.com/more/all"
    ]

    def parse(self, response):
        page = Selector(response)

        hrefs = page.xpath('//h4[@class="title"]/a/@href')

        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):

        page = Selector(response)
        item = AppstoreItem()
        item['title'] = page.xpath('//h4[@class="title"]/a/text()').extract_first().encode('utf-8')
        item['url'] = page.xpath('//h4[@class="title"]/a/@href').extract_first()
        appid = re.match(r'http://.*/(.*)', item['url']).group(1)
        item['appid'] = appid
        item['intro'] = page.xpath('//p[@class="content"]/text()').extract_first().encode('utf-8')

        divs = page.xpath('//div[@class="open-info"]')
        recomm = ""

        for div in divs:
            url = divs.xpath('./p[@class="name"]/a/@href').extract_first()
            recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
            name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
            recomm += "{0}:{1}, ".format(recommended_appid, name)

        item['recommended'] = recomm
        yield item