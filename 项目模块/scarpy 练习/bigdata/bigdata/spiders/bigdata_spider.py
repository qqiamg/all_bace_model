# -*- coding: utf-8 -*-
import scrapy


class BigdataSpiderSpider(scrapy.Spider):
    name = 'bigdata_spider'
    allowed_domains = ['bigdata.yisurvey.com']
    start_urls = ['http://bigdata.yisurvey.com/']

    def start_requests(self):
        start_urls = 'http://bigdata.yisurvey.com/commodity/market/'
        yield scrapy.Request(start_urls, self.parse)

    def parse(self, response):
        # 获取url
        all_bace_msg = response.xpath('//*[@class="wares"]/div/div[@class="splb"]/div/div[@class="list_text"]')
        for one_msg in all_bace_msg:
            name = one_msg.xpath('./h3/text()').extract_first()
            details_url = 'http://bigdata.yisurvey.com/' + one_msg.xpath('./a/@href').extract_first()
            yield scrapy.Request(details_url, callback=self.parse_details,
                                 meta={'item': {'name': name, 'details_url': details_url}})

    def parse_details(self, response):
        data_item = response.meta.get('item')
        # print(data_item)
        upload_time = response.xpath('//*[@class="mar_rt"]//span[contains(text(),"上架时间")]/text/text()').extract_first()
        update_time = response.xpath('//*[@class="mar_rt"]//span[contains(text(),"更新时间")]/text/text()').extract_first()
        money = response.xpath('//*[@class="mar_rt"]//span[contains(text(),"价格")]/text/text()').extract_first()
        using = response.xpath('//*[@class="mar_rt"]//span[contains(text(),"使用量")]/text/text()').extract_first()
        introduction = response.xpath('//*[@class="storeed"]/p/text()').extract_first()
        item = {
            'upload_time': upload_time,
            'update_time': update_time,
            'money': money,
            'using': using,
            'introduction': introduction,
            'dietail_url': data_item.get('details_url')
        }
        # print(item)
        yield item