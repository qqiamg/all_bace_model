# -*- coding: utf-8 -*-
import time
import smtplib
import logging
import os
import datetime
import pymongo
import requests
import socket
import re

from twisted.internet import task

from email.mime.text import MIMEText
# from scrapy.conf import settings
from scrapy.utils.engine import get_engine_status #旧
from scrapy.utils.project import get_project_settings #新版写法
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class RedisSpiderSmartIdleClosedExensions(object):

    def __init__(self, idle_number, crawler):
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查是否应该启用和提高扩展
        # 否则不配置
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # 获取配置中的时间片个数，默认为360个，30分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 360)

        # 实例化扩展对象
        ext = cls(idle_number, crawler)

        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s redis spider Idle, Continuous idle limit： %d", spider.name, self.idle_number)

    def spider_closed(self, spider):
        logger.info("closed spider %s, idle count %d , Continuous idle count %d",
                    spider.name, self.idle_count, len(self.idle_list))

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数

        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_number:
            # 连续触发的次数达到配置次数后关闭爬虫
            logger.info('\n continued idle number exceed {} Times'
                        '\n meet the idle shutdown conditions, will close the reptile operation'
                        '\n idle start time: {},  close spider time: {}'.format(self.idle_number,
                                                                                self.idle_list[0], self.idle_list[0]))

            # 先发送请求获取ip
            # try:
            #     url = 'http://www.baidu.com/s?wd=ip%E5%9C%B0%E5%9D%80'  # 找百度拿ip地址
            #     res = requests.get(url, timeout=15).text
            #
            #     real_ip = re.findall('本机IP:(.*?)<', res)[0].replace("&nbsp;", "")
            # except:
            #     url = 'http://pv.sohu.com/cityjson?ie=utf-8'  # 访问搜狐拿ip
            #     try:
            #         res = requests.get(url, timeout=15).text
            #         real_ip = re.findall('"cip": "(.*?)",', res)[0]
            #     except:
            #         real_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))  # 两者都拿不到就用本机Ip

            # rh = settings["REDIS_HOST"]  # redis_host
            # rp = settings["REDIS_PORT"]  # redis_port
            # end_url = "http://114.55.238.250/console/finish_crawler/?rh={}&rp={}".format(rh, rp)
            # res = requests.get(end_url)
            # table_name = spider.crawler_table_name
            # res_end = requests.get("http://114.55.238.250/console/local/result/?table={}".format(table_name))

            # 执行关闭爬虫操作
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')


class End58(object):
    """
    58爬虫结束删除TTf和xml
    """

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def __init__(self, crawler):
        self.crawler = crawler

    def spider_closed(self, spider):
        os.remove("58.ttf")
        os.remove("58.xml")


class DBStats(object):
    """Log basic scraping stats periodically
        统计信息日志写进mongodb
    """

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, crawler, interval)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def __init__(self, stats, crawler, interval=60.0):
        self.stats = stats
        self.interval = interval
        self.multiplier = 60.0 / self.interval
        self.task = None
        self.crawler = crawler
        self.settings = get_project_settings()

    def spider_opened(self, spider):

        item = {}
        now_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
        msg = "爬虫运行开始"
        item["时间"] = now_time
        item["日志信息"] = msg
        # 插入mongodb
        host = self.settings['MONGODB_HOST']
        port = self.settings['MONGODB_PORT']
        self.client = pymongo.MongoClient(host=host, port=port)
        self.collection = self.client[self.settings['MONGODB_DB']]
        table_name = self.settings["LOG_TABLE"]
        collection_ = self.collection[table_name]
        collection_.insert_one(dict(item))
        self.pagesprev = 0
        self.itemsprev = 0
        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def log(self, spider):
        items = self.stats.get_value('item_scraped_count', 0)
        pages = self.stats.get_value('response_received_count', 0)
        irate = (items - self.itemsprev) * self.multiplier
        prate = (pages - self.pagesprev) * self.multiplier
        self.pagesprev, self.itemsprev = pages, items
        item = {}
        msg = "Crawled {} pages (at {} pages/min), " \
              "scraped {} items (at {} items/min)".format(pages, prate, items, irate)
        now_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
        item["时间"] = now_time
        item["日志信息"] = msg
        # 插入mongodb
        table_name = self.settings["LOG_TABLE"]
        collection = self.collection[table_name]
        collection.insert_one(dict(item))
        # logger.info(msg, log_args, extra={'spider': spider})

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()
        now_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
        item_list = []
        for i in spider.crawler.stats.get_stats().items():
            item = {}
            item["时间"] = now_time
            item["日志信息"] = '%s: %s' % i
            item_list.append(item)

        item = {}
        msg = "爬虫运行完毕"
        item["时间"] = now_time
        item["日志信息"] = msg
        item_list.append(item)

        # 插入mongodb
        table_name = self.settings["LOG_TABLE"]
        collection = self.collection[table_name]
        for item_one in item_list:
            collection.insert_one(dict(item_one))
        self.client.close()
        # rh = settings["REDIS_HOST"]  # redis_host
        # rp = settings["REDIS_PORT"]  # redis_port
        # end_url = "http://114.55.238.250/console/finish_crawler/?rh={}&rp={}".format(rh, rp)
        # res = requests.get(end_url)
        # # table_name = spider.crawler_table_name
        # res_end = requests.get("http://114.55.238.250/console/local/result/?table={}".format(table_name))