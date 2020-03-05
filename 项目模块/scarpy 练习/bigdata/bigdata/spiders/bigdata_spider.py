# -*- coding: utf-8 -*-
import scrapy


class BigdataSpiderSpider(scrapy.Spider):
    name = 'bigdata_spider'
    allowed_domains = ['bigdata.yisurvey.com']
    start_urls = ['http://bigdata.yisurvey.com/']

    def start_requests(self):
        start_urls = 'http://bigdata.yisurvey.com/commodity/market/'
        yield scrapy.Request(start_urls,self.parse)

    def parse(self, response):
        all_bace_msg = response.xpath('//*[@class="wares"]/div/div[@class="splb"]/div/div[@class="list_text"]')
        for one_msg in all_bace_msg:
            name = one_msg.xpath('./h3/text()').extract_first()
            url = 'http://bigdata.yisurvey.com/' + one_msg.xpath('./a/@href').extract_first()


