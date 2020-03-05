# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
# from baidu.items import HuiCItem

class ComSpiderSpider(scrapy.Spider):
    name = 'com_spider'
    allowed_domains = ['hc360.com']
    start_urls = ['https://s.hc360.com/']

    def start_requests(self):
        start_url = 'https://s.hc360.com/seller/search.html?kwd=LED%E7%81%AF&c=&F=&G=&nselect=1&pnum=1'
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        data = response.xpath('//*[@class="wrap-grid"]//li')
        for i in data:


        # for num in range(1,data+1):
        #     # 需要实例化ItemLoader， 注意第一个参数必须是实例化的对象...
        #     atricleItemLoader = ItemLoader(item=HuiCItem(),response=response)
        #     # 调用xpath选择器，提起title信息
        #     atricleItemLoader.add_xpath('title',f'//*[@class="wrap-grid"]//li[{num}]/div/div[@class="seaNewList"]/dl/dd[@class="newName"]/a/text()')
        #     # 将提取好的数据load出来
        #     articleInfo = atricleItemLoader.load_item()
        #     # title = one_data.xpath('./div/div[@class="seaNewList"]/dl/dd[@class="newName"]/a/text()').extract_first('')
        #     # print(title)
        # atricleItemLoader = ItemLoader(item=HuiCItem(), response=response)
        # # 调用xpath选择器，提起title信息
        # atricleItemLoader.add_xpath('title',
        #                             f'//*[@class="wrap-grid"]//li[@class="grid-list"]/div/div[@class="seaNewList"]/dl/dd[@class="newName"]/a/text()')
        # # 将提取好的数据load出来
        # articleInfo = atricleItemLoader.load_item()
        # print(f"articleInfo = {articleInfo}")

