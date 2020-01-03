import re
import time
import os
import datetime

import paramiko
import requests
import oss2
from itertools import islice
import os
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import xlrd
from lxml import etree
from fuzzywuzzy import fuzz
import pymysql
from common import get_code


class Hipac(object):
    def __init__(self, ):
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1300, 1000)
        self.browser.set_script_timeout(30)
        self.browser.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.browser, 30)
        self.d = {}  # 保存搜索结果页的商品信息的字典（包含所有的搜索结果）
        self.com_d = {}  # 保存产品信息的结果
        self.SKU_list = []  # 保存客户所给的SKU关键词
        self.kw_list = []  # 自己组装的关键词
        self.search_num = 1  # 和搜索表id组装保持唯一性
        self.info_num = 1

    def run(self):
        self.open_web()
        n = 0
        while True:
            state = self.login()
            if state:
                break
            if n >=5:
                break
            n += 1



    def open_web(self):
        try:
            self.browser.get('https://mall.hipac.cn/mall/view/login/login.html')
        except Exception as e:
            print('登陆错误：{}'.format(e))

    """进行模拟登陆"""

    def login(self):
        try:
            input_opd1 = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#username')))  # 账户名
            input_opd1.clear()
            input_opd1.send_keys('15994964066')

            input_opd2 = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#passworda')))  # 密码
            input_opd2.clear()
            input_opd2.send_keys('a1234567')
            input_kw = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#kaptcha')))  # 验证码
            input_kw.clear()
            cookies = self.browser.get_cookies()
            page_rs = self.browser.page_source
            html = etree.HTML(page_rs)
            if html.xpath('//img[@id="kaptchaImage"]/@src'):
                yz_url = 'https:'+html.xpath('//img[@id="kaptchaImage"]/@src')[0]
            else:
                return False
            print(cookies)
            text_list = []
            for cookie in cookies:
                # print(cookie['name'], cookie['value'])
                text_list.append('{}={}'.format(cookie['name'], cookie['value']))
            cookies_str = '; '.join(text_list)
            print(cookies_str)
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                'Cookie':cookies_str
            }
            rs = requests.get(yz_url,headers=headers,timeout=20).content
            file_path = './' + '{file_name}.{file_suffix}'.format(
                file_name= '1',
                file_suffix='jpg')

            with open(file_path, 'wb') as f:
                f.write(rs)
                print('Downloaded image path is %s' % file_path)

            V_code = get_code()
            if V_code:
                input_kw.send_keys(V_code)
                button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginUserBtn')))  # 点击登录按钮
                button.click()
                response = self.browser.page_source
                html = etree.HTML(response)
                if html.xpath('//img[@id="kaptchaImage"]/@src'):
                    return False
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

hipac = Hipac()
hipac.run()