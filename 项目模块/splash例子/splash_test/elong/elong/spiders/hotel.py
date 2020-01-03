# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy_redis.spiders import RedisSpider
import urllib.parse


class HotelSpider(RedisSpider):
    name = 'hotel'
    allowed_domains = ['elong.com']
    # url = 'http://hotel.elong.com/huangshan/?tdsourcetag=s_pcqq_aiomsg'
    redis_key = 'elong:start_urls'

    def make_requests_from_url(self, url):
        start_script = """
                            function main(splash, args)
                                 assert(splash:go(args.url))
                                 assert(splash:wait(args.wait))
                                 return splash:html()
                             end
                """
        return SplashRequest(url, callback=self.parse, endpoint='execute',
                             args={'lua_source': start_script, 'wait': 3},
                             meta={'netloc': urllib.parse.urlparse(url).netloc,
                                   "scheme": urllib.parse.urlparse(url).scheme})

    def parse(self, response):
        # print(response.text)
        netloc = response.meta.get("netloc")
        scheme = response.meta.get("scheme")
        hotel_list = response.xpath('//*[@class="info_cn"]')
        num = 1
        for i in hotel_list:
            hotel_url = scheme + "://" + netloc + i.xpath("./../@href").extract_first()
            print(hotel_url)
            script = """
                                        function main(splash, args)
                                             assert(splash:go(args.url))
                                             assert(splash:wait(args.wait))
                                             return splash:html()
                                         end
                            """
            yield SplashRequest(hotel_url, callback=self.parse_detail, endpoint='execute',
                                args={'lua_source': script, 'wait': 10}, meta={"num": num})
            num += 1

    def parse_detail(self, response):
        num = response.meta.get("num")
        print(num)
        bed_list = response.xpath('//*[@class="bedname"]/text()').extract
        print(bed_list)
        for i in bed_list:
            bed_name = i.xpath("./text()").extract_first()
            yield bed_name
