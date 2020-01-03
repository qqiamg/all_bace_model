# -*- coding: utf-8 -*-

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

import scrapy, json, re, os
import urllib.parse
from pyquery import PyQuery as pq
import datetime
import time

from scrapy_redis.spiders import RedisSpider


class CompanySpider(RedisSpider):
    name = 'company_data'
    allowed_domains = ['xin.baidu.com']

    def __init__(self,  *args, **kwargs):
        super(CompanySpider, self).__init__(*args, **kwargs)
        self.redis_key = "yellow_page:start_urls"
        self.crawler_table_name = "baidu_directory"

    def parse(self, response):
        """
        进入百度信用关键词搜索页
        :param response:
        :return:
        """
        # 获取用户uid，防止后面返回的url错误,开始获取第一页微博
        # uid = response.meta.get("uid")
        company_list = response.xpath('//div[@class="zx-list-item"]')
        if company_list:
            company_href = response.xpath(
                '//div[@class="zx-list-item"][1]//a[@class="zx-list-item-url"]/@href').extract_first()
            # print(company_href)
            pid_ = company_href.split("?")[1]  # 拿出pid，请求json
            # print(pid_)
            url = 'https://xin.baidu.com/detail/basicAjax?{pid}&_={times}&fl=1&castk=LTE%3D'.format(pid=pid_, times=int(
                time.time() * 1000))
            # print(url)
            yield scrapy.Request(url, callback=self.parse_data)

    def parse_data(self, response):
        res_json = json.loads(response.text)
        data = res_json['data']
        item = {}
        item["公司名字"] = data['entName']
        item["电话"] = data["telephone"]
        item["邮箱"] = data['email']
        item["官网"] = data['claimUrl']
        item["地址"] = data["regAddr"]
        item["简介"] = data["describe"]
        item["注册资本"] = data['regCapital']
        item["实缴资本"] = data["paidinCapital"]
        item["法定代表人"] = data["legalPerson"]
        item["经营状态"] = data["openStatus"]
        item["曾用名"] = data["prevEntName"]
        item["所属行业"] = data["industry"]
        item["统一社会信用代码"] = data["unifiedCode"]
        item["纳税人识别号"] = data["taxNo"]
        try:
            item["工商注册号"] = data["licenseNumber"]
        except:
            item["工商注册号"] = ''
        item["组织机构代码"] = data["orgNo"]
        item["登记机关"] = data["authority"]
        item["成立日期"] = data["startDate"]
        item["企业类型"] = data["entType"]
        item["营业期限"] = data["openTime"]
        item["行政区划"] = data["district"]
        item["审核/年检日期"] = data["annualDate"]
        item["注册地址"] = data["regAddr"]
        item["经营范围"] = data["scope"]
        yield item
        # company_name = response.xpath('//span[@class="entName"]/text()').extract_first(default='')  # 公司名字
