from scrapy import cmdline
import os
dir = r'D:\杨伟强\整理\项目模块\scarpy 练习\baidu\baidu\spiders'

os.chdir(dir)
# command = 'scrapy crawl mweibo'
# command = 'scrapy crawl company_data'
command = 'scrapy crawl com_spider'

cmdline.execute(command.split())

# from scrapy import cmdline
# args = "scrapy crawl com_spider.py".split()
# cmdline.execute(args)