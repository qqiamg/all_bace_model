import requests, os, json, base64
from scrapy.selector import Selector
from binascii import hexlify
from Crypto.Cipher import AES
import pymongo
import time
import openpyxl
import wordcloud
import re
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

# 获取评论
class GetComment():
    def __init__(self, song_id):
        self.id = 1403921413
        self.headers = {
            'origin': 'https://music.163.com',
            'referer': 'https://music.163.com/song?id={}'.format(self.id),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }
        self.ep = Encrypyed()
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.page = 21
        self.db = self.client['网易云']
        self.collection = self.db['看见你的声音']

    @staticmethod
    def proxies_api(proxyUser, proxyPass):
        '''
        :param proxyUser: 阿布云生成用户
        :param proxyPass: 阿布云生成密码
        :return: 代理信息
        '''
        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = proxyUser
        proxyPass = proxyPass
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    def get_comment(self, offset):
        comment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(self.id)
        text = {'rid': "R_SO_4_{}".format(self.id), 'offset': "{}".format(offset), 'total': "true", 'limit': "100",
                'csrf_token': ""}
        data = self.ep.search(text)
        # res = requests.post(comment_url,data=data,headers =self.headers,verify=False)
        res = self.retry_post(comment_url, self.headers, data, 20)
        if res:
            json_msg = res.json()
            tag = self.jiexi(json_msg)
            return tag
        else:
            print(res.text)
            return 'stop'
        # print(data)

    def retry_post(self, url, headers, data, count):
        try:
            response = requests.post(url, headers=headers, data=data,
                                     proxies=self.proxies_api('H5Q5P1972OE72Q6D', 'D662875D552416BF'), timeout=10)
            if response.status_code == 200:
                print('成功')
                return response
            a = response.text
            raise Exception
        except Exception as e:
            if count < 10:
                print(count)
                response = self.retry_post(url, headers, data, count + 1)
                return response
            else:
                print(count)
                print(e)
                return None

    def jiexi(self, json_msg):
        comments = json_msg.get('comments')
        if comments:
            print('评论数：', str(len(comments)))
            for one_comment in comments:
                user_name = one_comment.get('user').get('nickname')
                user_id = one_comment.get('user').get('userId')
                comment = one_comment.get('content')
                like_count = one_comment.get('likedCount')
                time_stamp = one_comment.get('time')
                if time_stamp:
                    a = time.localtime(int(time_stamp / 1000))
                    c_time = time.strftime("%Y-%m-%d %H:%M:%S", a)
                else:
                    c_time = ''
                if one_comment.get('beReplied'):
                    is_bereplied = True
                    bereplie_comment = one_comment.get('beReplied')[0].get('content')
                else:
                    is_bereplied = False
                    bereplie_comment = ''
                item = {
                    'user_name': user_name,
                    'user_id': user_id,
                    'comment': comment,
                    'like_count': like_count,
                    'c_time': c_time,
                    'is_bereplied': is_bereplied,
                    'bereplie_comment': bereplie_comment,
                    'page': self.page
                }
                # print(item)
                self.collection.insert(item)
        else:
            return 'stop'

    def run(self):

        while True:
            print('第{}页'.format(self.page + 1))
            time.sleep(1)
            flag = self.get_comment(20 * self.page)
            if flag == 'stop':
                break
            self.page += 1
            # break


# 解析参数
class Encrypyed():
    '''传入歌曲的ID，加密生成'params'、'encSecKey 返回'''

    def __init__(self):
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'

    def create_secret_key(self, size):
        # print(hexlify(os.urandom(size))[:16].decode('utf-8'))
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    def aes_encrypt(self, text, key):
        iv = b'0102030405060708'
        pad = 16 - len(text) % 16
        # print(len(text))
        # print(pad)
        text = text + pad * chr(pad)
        # print(text)
        encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        result = encryptor.encrypt(text.encode('utf-8'))
        # print(result)
        # print(bytes.decode(result))
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]  # 倒序
        rs = pow(int(hexlify(text.encode('utf-8')), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def work(self, ids, br=128000):
        text = {'ids': [ids], 'br': br, 'csrf_token': ''}
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        return data

    def search(self, text):
        text = json.dumps(text)
        i = self.create_secret_key(16)  # 随机16位字符串
        # print('i:',i)
        encText = self.aes_encrypt(text, self.nonce)  # 使用AES加密，模式为CBC
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)  # 加密文本为随机字符串i,他的公钥是第二个参数，模式是第三个参数
        data = {'params': encText, 'encSecKey': encSecKey}
        return data

#绘制词云图片
class WritePhoto():
    def __init__(self):
        pass

    def get_photo(self):
        all_comment = self.read_excel('Last Dance.xlsx')
        sub_comment = re.sub('\[.*?\]','',all_comment)      #除去表情
        # print(sub_comment)
        alice_mask = np.array(Image.open("未命名_meitu_3.png"))
        w = wordcloud.WordCloud(background_color='white',mask=alice_mask,max_words=2000)
        w.generate(sub_comment)
        w.to_file('1.jpg')
        # plt.imshow(w)


    def read_excel(self, excel_name):
        '''
        读取excel操作（复制到自身代码操作）
        :param excel_name: excel的名字
        :return:
        '''
        name = excel_name
        wb = openpyxl.load_workbook(name)
        ws = wb.active
        rows = ws.rows
        count = 0
        start = 1  # 通过调整 start 的值进行选择第几行excel开始读取, 1 为第二行开始读取
        all_comment = []
        for j, row in enumerate(rows):
            if count < start:
                count += 1
                continue
            # print(j)
            # print(row[4].value)  # row[0].value 为当前行第一个单元格的值
            all_comment.append(row[4].value)
        return ' '.join(all_comment)


if __name__ == '__main__':
    # a = GetComment(123)
    # a.run()
    a =WritePhoto()
    a.get_photo()
