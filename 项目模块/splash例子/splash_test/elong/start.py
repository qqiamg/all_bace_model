from scrapy import cmdline
import os
dir = r'C:\Users\00000\Desktop\splash_test\elong\elong\spiders'

os.chdir(dir)
# command = 'scrapy crawl mweibo'
# command = 'scrapy crawl hotel'
command = 'scrapy runspider hotel.py'

cmdline.execute(command.split())