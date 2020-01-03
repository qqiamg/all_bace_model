import datetime
import random
import re
import time

import requests
import pymongo
from lxml import etree


class DGDianping():
    '''
    处理评论和电话的字体问题
    '''
    font_size = 14
    start_y = 23
    address_y = 15
    def __init__(self, shop_id_iist, cookies, delay=7):
        '''
        :param shop_id_iist: 需抓取的店铺id列表
        :param cookies:     传入一个cookie
        :param delay:   延时基础值
        '''
        self.shop_id_list = shop_id_iist
        self._delay = delay
        self.font_ydict = {}  # 评论字典坐标
        self.num_ydict = {}  # 数字字典坐标
        self.address_ydict = {}  # 地址字典坐标
        self.font_dict = {}
        self.num_ = {}
        self.address_ = {}
        self._cookies = self._format_cookies(cookies)
        self._css_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
        self._default_headers = {
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
        # self._cur_request_url = 'http://www.dianping.com/shop/{}/review_all/p1'.format(shop_id)
        # self._cur_request_css_url = 'http://www.dianping.com/shop/{}/'.format(shop_id)
        self.err_list = []
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        # 指定数据库
        self.db = self.client['大众点评']
        # 指定集合(类似表)
        # self.collection = self.db['王品牛排']
        self.err = self.db['错误']
        self.get_time = 1

    def _get_css_link(self):
        """
            一、请求评论首页，获取css样式文件
        """
        url = 'http://www.dianping.com/shop/{}/review_all/p1'.format('127831717')
        res = requests.get(url, headers=self._default_headers, cookies=self._cookies)
        html = res.text
        # print('首页源码', html)
        # css_link = re.search(r'<link re.*?css.*?href="(.*?svgtextcss.*?)">', html)
        css_link = re.findall(r'<link rel="stylesheet" type="text/css" href="//s3plus.meituan.net/v1/(.*?)">', html)
        assert css_link
        css_link = 'http://s3plus.meituan.net/v1/' + css_link[0]
        print('css链接', css_link)
        return css_link

    def _get_num_dict_by_offset(self, url):
        """
            二、 获取坐标偏移的文字字典, 会有最少两种形式的svg文件（目前只遇到两种）（数字）
        """
        for one_link in url:
            urls = 'http:' + one_link
            res = requests.get(urls, timeout=60)
            html = res.text
            num_dict = {}
            font_dict = {}
            y_list = re.findall(r'd="M0 (\d+?) ', html)
            if y_list:
                font_list = re.findall(r'<textPath .*?>(.*?)<', html)
                if len(font_list) < 15:
                    print('为地址信息')
                    for i, string in enumerate(font_list):
                        y_offset = self.start_y - int(y_list[i]) - 8
                        sub_font_dict = {}
                        for j, font in enumerate(string):
                            x_offset = -j * self.font_size
                            sub_font_dict[x_offset] = font
                        self.address_ydict[y_offset] = sub_font_dict
                        # continue
                else:
                    print('为评论信息')
                    for i, string in enumerate(font_list):
                        y_offset = self.start_y - int(y_list[i])
                        sub_font_dict = {}
                        for j, font in enumerate(string):
                            x_offset = -j * self.font_size
                            sub_font_dict[x_offset] = font
                        self.font_ydict[y_offset] = sub_font_dict
            #地址未处理
            else:
                font_list = re.findall(r'<text.*x="(.*?)".*?y="(.*?)">(.*?)<', html)
                x_list = font_list[0][0].split(' ')
                # print(x_list)
                # input(12312)
                if len(x_list) > 2:
                    print('为数字列表')
                    for x, y, string in font_list:
                        y_offset = 15 - int(y)
                        sub_num_dict = {}
                        x_list = x.strip().split(' ')
                        for j, font in enumerate(string):
                            x_offset = -(int(x_list[j]) - 6)
                            sub_num_dict[x_offset] = font
                            # print(sub_font_dict)
                        self.num_ydict[y_offset] = sub_num_dict

                else:
                    print('为文字列表')
                    if len(font_list) <15:
                        print('为地址列表')
                        for x, y, string in font_list:
                            y_offset = self.address_y - int(y)
                            sub_font_dict = {}
                            for j, font in enumerate(string):
                                x_offset = -j * self.font_size
                                sub_font_dict[x_offset] = font
                            self.address_ydict[y_offset] = sub_font_dict
                            print(self.address_ydict)
                    else:
                        print('为评论列表')
                        for x, y, string in font_list:
                            y_offset = self.start_y - int(y)
                            sub_font_dict = {}
                            for j, font in enumerate(string):
                                x_offset = -j * self.font_size
                                sub_font_dict[x_offset] = font
                            self.font_ydict[y_offset] = sub_font_dict
        print('字体字典', self.font_ydict)
        print('地址字典', self.address_ydict)
        print('数字字典', self.num_ydict)
        return [self.font_ydict, self.num_ydict, self.address_ydict]

    def _get_num_dict(self, url):
        """
           三、根据获取到的坐标进行获取css样式对应文字的字典
        """
        print('解析svg成字典的css', url)
        res = requests.get(url, headers=self._css_headers, cookies=self._cookies, timeout=60)
        html = res.text
        # print(html)
        background_image_link = re.findall('background-image: url\((.*?)\);', html)
        print('带有svg的链接', background_image_link)
        assert background_image_link
        background_image_link = background_image_link
        print(background_image_link)
        html = re.sub(r'span.*?\}', '', html)
        group_offset_list = re.findall(r'\.([a-zA-Z0-9]{5,6}){.*?round:(.*?)px (.*?)px;', html)  # css中的类
        print('css中class对应坐标', group_offset_list)
        font_dict_by_offset = self._get_num_dict_by_offset(background_image_link)  # svg得到这里面对应成字典
        # print('解析svg成字典', font_dict_by_offset)
        self.err_class_name = [[], [], []]  # 电话，评论，地址
        # num_dict_by_offset = font_dict_by_offset[1]
        # cfont_dict_by_offset = font_dict_by_offset[0]
        # for class_name, x_offset, y_offset in group_offset_list:
        #     y_offset = y_offset.replace('.0', '')
        #     x_offset = x_offset.replace('.0', '')
        #     # print(y_offset,x_offset)
        #     if num_dict_by_offset.get(int(y_offset)):  # 数字匹配
        #         try:
        #             self.num_[class_name] = num_dict_by_offset[int(y_offset)][int(x_offset)]
        #         except:
        #             err_class_name.append(class_name)
        #             pass
        #     if cfont_dict_by_offset.get(int(y_offset)):  # 评论文字匹配
        #         try:
        #             self.font_dict[class_name] = cfont_dict_by_offset[int(y_offset)][int(x_offset)]
        #         except:
        #             err_class_name.append(class_name)
        #             pass
        # if 'cf121' in err_class_name:
        #     self.font_dict['cf121'] = '的'
        # if 'cfozf' in err_class_name:
        #     self.font_dict['cfozf'] = '道'
        # self.font_dict['hn3jq'] = '原'
        # self.font_dict['hniub'] = '盆'
        self.matching_all_mes(font_dict_by_offset, group_offset_list)  # 把标识和字体匹配
        print(self.font_dict)  # 评论字典
        print(self.address_)  # 地址字典
        print(self.num_)  # 号码字典
        print(self.err_class_name)
        input(1111)
        # return [self.num_, self.font_dict]

    def get_all_dict(self):
        '''获取字体字典'''
        self._css_link = self._get_css_link()
        print('css 的连接', self._css_link)
        self._get_num_dict(self._css_link)  # 评论和电话的文字

    def _get_page(self, id):  # 获得评论内容
        """
            请求电话，并将<cc></cc>样式替换成文字
            请求评论，并将<svgmtsi></svgmtsi>样式替换
            请求地址，并将<bb></bb>样式替换
        """
        self._cur_request_url = 'http://www.dianping.com/shop/{}/review_all/p1'.format(id)
        while self._cur_request_url:
            print('错误列表')
            print(len(self.err_list))
            self._delay_func()
            print('[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=self._cur_request_url))
            try:
                res = requests.get(self._cur_request_url, headers=self._default_headers, cookies=self._cookies,
                                   timeout=60)
            except:
                continue
            # 判断是否出现验证码
            class_set_font = set()
            self.html = res.text
            for span in re.findall(r'<svgmtsi class="([a-zA-Z0-9]{5,6})"></svgmtsi>', self.html):
                class_set_font.add(span)
            if len(class_set_font):
                pass
            else:
                print('出验证码')
                input(11)
                continue
            # 替换数字部分
            self.replace_num(res)
            # 替换评论文字部分
            self.replace_font(res)
            # 替换地址部分
            self.replace_adress(res)
            doc = etree.HTML(self.html)
            self._parse_page(doc, self._cur_request_url)
            # 下方这一块为获取下一页链接，如只拿电话请注释 直接 break 循环
            try:
                self._default_headers['Referer'] = self._cur_request_url
                next_page_url = 'http://www.dianping.com' + doc.xpath('.//a[@class="NextPage"]/@href')[0]
            except IndexError:
                next_page_url = None
                self.get_time = 1
                break
            self._cur_request_url = next_page_url

    def _parse_page(self, doc, url):
        """
            解析页面并提取数据
        """
        # self.item = {}
        shop_name = doc.xpath('//*[@class="review-shop-wrap"]//h1[@class="shop-name"]/text()')[0]
        phone = self.get_phone(doc)  # 拿电话
        # input(111)
        address = self.get_address(doc)  # 拿地址
        item = {
            '店名': shop_name,
            '电话': phone,
            '地址': address
        }
        if self.get_time == 1:
            self.collection = self.db[shop_name]
            self.get_time = 2
        print(item)
        self.get_comment(item, doc, url)  # 拿评论
        # print(self.item)
        # self._data_pipeline(data)

    def get_phone(self, doc):
        '''获取电话'''
        phone1 = ''.join(doc.xpath('//*[@class="phone-info"]//text()')).replace('电话:', '').strip('\n\r \t')
        phone = phone1.replace('\xa0','')
        # self.item['电话'] = phone
        return phone

    def get_address(self, doc):
        adress1 = ''.join(doc.xpath('//*[@class="address-info"]//text()')).replace('地址:', '').replace('\n', '').strip(
            '\n\r \t')
        adress = adress1.strip()
        return adress

    def get_comment(self, bace_item, doc, url):
        for li in doc.xpath('//*[@class="reviews-items"]/ul/li'):
            item = {}
            name = li.xpath('.//a[@class="name"]/text()')[0].strip('\n\r \t')
            try:
                star = li.xpath('.//span[contains(./@class, "sml-str")]/@class')[0]
                star = re.findall(r'sml-rank-stars sml-str(.*?) star', star)[0]
            except IndexError:
                star = 0
            time = li.xpath('.//span[@class="time"]/text()')[0].strip('\n\r \t')
            pics = []

            if li.xpath('.//*[@class="review-pictures"]/ul/li'):
                for pic in li.xpath('.//*[@class="review-pictures"]/ul/li'):
                    # print(pic.xpath('.//a/@href'))
                    pics.append(pic.xpath('.//a/img/@data-big')[0])
            comment = ''.join(li.xpath('.//div[@class="review-words Hide"]/text()')).strip('\n\r \t')
            if not comment:
                comment = ''.join(li.xpath('.//div[@class="review-words"]/text()')).strip('\n\r \t')
            item['name'] = name
            item['comment'] = comment
            item['star'] = star
            item['pic'] = pics
            item['time'] = time
            item['url'] = url
            # print(item)
            item.update(bace_item)
            self._data_pipeline(item)

    def _data_pipeline(self, data):
        """
            处理数据
        """
        self.collection.insert(data)
        print('最终数据:', data)

    def replace_font(self, res):
        '''
        替换评论字体
        :param html: 解析的需处理的页面源码
        :param res: 原始页面
        :return: 
        '''
        # 替换评论
        class_set_font = set()
        for span in re.findall(r'<svgmtsi class="([a-zA-Z0-9]{5,6})"></svgmtsi>', self.html):
            class_set_font.add(span)
        if len(class_set_font):
            pass
        for class_name in class_set_font:
            # print(self._font_dict[class_name])
            try:
                self.html = re.sub('<svgmtsi class="%s"></svgmtsi>' % class_name, self.font_dict[class_name], self.html)
            except:
                print('评论文字匹配失败')
                # print(res.text)
                print(class_name)
                self.html = re.sub('<svgmtsi class="%s"></svgmtsi>' % class_name, '({})'.format(class_name), self.html)
                item = {
                    'url': self._cur_request_url,
                    'class_name': class_name,
                    '源码': str(res.text)
                }
                try:
                    self.err.insert(item)
                except Exception as e:
                    print(e)
                    pass
                self.err_list.append(item)
                # return htmls

    def replace_num(self, res):
        '''
        替换数字
        :param html: 解析的需处理的页面源码
        :param res: 原始页面
        :return: 
        '''
        # 替换数字
        class_set = set()
        for span in re.findall(r'<cc class="([a-zA-Z0-9]{5,6})"></cc>', self.html):
            class_set.add(span)
        if len(class_set):
            pass
        for class_name in class_set:
            # print(self._font_dict[class_name])
            try:
                self.html = re.sub('<cc class="%s"></cc>' % class_name, self.num_[class_name], self.html)
                # print('数字替换成功')
            except:
                print('数字替换失败')
                # print(res.text)
                print(class_name)
                self.html = re.sub('<cc class="%s"></cc>' % class_name, '({})'.format(class_name), self.html)
                item = {
                    'url': self._cur_request_url,
                    'class_name': class_name,
                    '源码': str(res.text)
                }
                try:
                    self.err.insert(item)
                except Exception as e:
                    print(e)
                    pass
                self.err_list.append(item)
                # return htmls

    def replace_adress(self, res):
        '''
                替换地址
                :param html: 解析的需处理的页面源码
                :param res: 原始页面
                :return: 
                '''
        # 替换数字
        class_set = set()
        for span in re.findall(r'<bb class="([a-zA-Z0-9]{5,6})"></bb>', self.html):
            class_set.add(span)
        if len(class_set):
            pass
        for class_name in class_set:
            # print(self._font_dict[class_name])
            try:
                self.html = re.sub('<bb class="%s"></bb>' % class_name, self.address_[class_name], self.html)
                # print('数字替换成功')
            except:
                print('地址替换失败')
                # print(res.text)
                print(class_name)
                self.html = re.sub('<bb class="%s"></bb>' % class_name, '({})'.format(class_name), self.html)
                item = {
                    'url': self._cur_request_url,
                    'class_name': class_name,
                    '源码': str(res.text)
                }
                try:
                    self.err.insert(item)
                except Exception as e:
                    print(e)
                    pass
                self.err_list.append(item)

    def matching_all_mes(self, font_dict_by_offset, group_offset_list):
        '''
        把标识和字体匹配
        :param font_dict_by_offset: 所有字体的坐标对应（评论，号码）
        :param group_offset_list: 所有坐标对应的标识
        :return: 
        '''
        num_dict_by_offset = font_dict_by_offset[1]
        cfont_dict_by_offset = font_dict_by_offset[0]
        address_dict_by_offset = font_dict_by_offset[2]
        print(group_offset_list)
        # input(111)
        for class_name, x_offset, y_offset in group_offset_list:
            y_offset = y_offset.replace('.0', '')
            x_offset = x_offset.replace('.0', '')
            # print(y_offset,x_offset)
            if num_dict_by_offset.get(int(y_offset)):  # 数字匹配
                try:
                    self.num_[class_name] = num_dict_by_offset[int(y_offset)][int(x_offset)]
                except:
                    self.err_class_name[0].append(class_name)
                    pass
            if cfont_dict_by_offset.get(int(y_offset)):  # 评论文字匹配
                try:
                    # if int(y_offset) == -947:
                    #     print(x_offset)
                    self.font_dict[class_name] = cfont_dict_by_offset[int(y_offset)][int(x_offset)]
                except:
                    self.err_class_name[1].append(class_name)
                    pass
            if address_dict_by_offset.get(int(y_offset)):  # 地址文字匹配
                try:
                    self.address_[class_name] = address_dict_by_offset[int(y_offset)][int(x_offset)]
                except:
                    # try:
                    # self.address_[class_name] = address_dict_by_offset[int(y_offset)][int(x_offset)]
                    self.err_class_name[2].append(class_name)
                    pass

    def _format_cookies(self, cookies):
        '''处理填入的cookie'''
        cookies = {cookie.split('=')[0]: cookie.split('=')[1]
                   for cookie in cookies.replace(' ', '').split(';')}
        return cookies

    def _delay_func(self):
        delay_time = random.randint((self._delay - 2) * 10, (self._delay + 2) * 10) * 0.1
        print('睡一会', delay_time)
        time.sleep(delay_time)

    def run(self):
        self.get_all_dict()  # 获取字体字典
        for one_id in self.shop_id_list:
            self._get_page(one_id)


if __name__ == "__main__":
    COOKIES = '_lxsdk_cuid=16eb00ed27ac8-0a145a2f788c5e-3b654406-1fa400-16eb00ed27ac8; _lxsdk=16eb00ed27ac8-0a145a2f788c5e-3b654406-1fa400-16eb00ed27ac8; _hc.v=ff89ebd1-4ef0-bd9f-b8ad-503cc36445ea.1574911793; ua=dpuser_4297777734; ctu=f99ecd3aee349826af7a81577860e828a93c233b8e9f7989a39831aedbca3f43; uamo=15112001518; cy=4; cye=guangzhou; lgtoken=0b432b422-8dcd-44b4-8499-6f92ec15a9dd; dper=3b20c4eae2e297421e2c60579d64fb167ce154ea786b3f62f878d2b9d4efd8c7c5b315faa043b012e9e656b30834687905e2d8e54ef891edce3038795a1a9a75177e3bb53d193e1cc7af8134c8cd95c27fefb20c9b2c09da545735ecb33935b9; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=16eb00ed27b-584-f17-1f2%7C%7C853'
    dp = DGDianping(['75164738'], cookies=COOKIES)
    dp.run()
