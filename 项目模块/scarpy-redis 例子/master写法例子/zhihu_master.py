import sys
import os
import redis
import urllib.parse


class RunMaster(object):
    def __init__(self, user_param, spider_name, crawler_table_name, file_name, redis_config):
        # 配置redis服务器
        self.redis_client = redis.StrictRedis(**redis_config)
        self.user_param = user_param
        self.spider_name = spider_name
        self.crawler_table_name = crawler_table_name
        self.file_name = file_name
        self.chose_mode = self.user_param["id"]

    def run(self):

        if self.chose_mode == 0:
            name = self.user_param["choice"][0]['param_values']
            try:

                start_url_list = name
                for start_url in start_url_list:
                    if "?" in start_url:
                        start_url = start_url.split("?")[0]
                    self.redis_client.lpush('{}:start_urls'.format(self.spider_name + str(self.crawler_table_name)),
                                            start_url)
                command = 'scrapy runspider {} -a spider_name={} -a crawler_table_name={}'.format(
                    self.file_name, self.spider_name, str(self.crawler_table_name))
                return command
            except:
                return False

    def gen_command(self):
        command = 'scrapy runspider {} -a spider_name={} -a crawler_table_name={}'.format(
            self.file_name, self.spider_name, str(self.crawler_table_name))
        return command
