# import requests
# #
# # url = 'https://cn-sh-cc-bcache-01.bilivideo.com/upgcxcode/09/56/156155609/156155609-1-16.mp4?e=ig8euxZM2rNcNbKBhwdVtWKBhwdVNEVEuCIv29hEn0lqXg8Y2ENvNCImNEVEUJ1miI7MT96fqj3E9r1qNCNEtodEuxTEtodE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==&uipk=5&nbs=1&deadline=1583603541&gen=playurl&os=bcache&oi=3753953192&trid=35153682d5884a16aff0bab07f276dd8u&platform=pc&upsig=18c0499d4e6ed68c86527e3e86ffcfb9&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=10789807&logo=40000000'
# # headers = {
# # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
# # "Accept-Encoding": "gzip, deflate, br",
# # "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
# # "Cache-Control": "max-age=0",
# # "Connection": "keep-alive",
# # "Cookie": "_uuid=859A75E6-69EC-D99D-6F64-AED3DD81F5AB81507infoc; buvid3=5411A56E-46AA-4B95-AA8F-8290FC903CEB190972infoc; CURRENT_FNVAL=16; rpdid=|(J~lJmlJkJJ0J'ulYlu|um|u; stardustvideo=1; LIVE_BUVID=AUTO2715672566367628; sid=4yyppgb6; _ga=GA1.2.506332833.1570102984; laboratory=1-1; im_notify_type_10789807=0; CURRENT_QUALITY=112; DedeUserID=10789807; DedeUserID__ckMd5=4219959445ef22ca; SESSDATA=04d4da14%2C1585392892%2C6bf4c321; bili_jct=16bb7cc234789f2fe0d3aac45f73b296; bp_t_offset_10789807=361626857529553955; INTVER=1; _dfcaptcha=5ef18a5ba50548dd880cc25e1e0a50be",
# # "Host": "api.bilibili.com",
# # "Upgrade-Insecure-Requests": "1",
# # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
# # }
# #
# # ss = requests.session()
# # res = ss.get('https://api.bilibili.com/x/player/playurl?avid=66476652&cid=115287880&fnval=0')
# # print(res.text)
# # ress = ss.get(url,headers=headers)
# # print(ress)
import requests
import os, sys


class BilibiliCrawler():
    def __init__(self, qn=80, output=''):
        # 初始化

        if output:
            path = os.getcwd() + '\\'
            path += output
            if not os.path.exists(path):
                os.mkdir(path)
                output = path + '\\'

        self.qn = qn
        self.output = output
        self.cid_url = 'https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp'
        self.flv_url = 'https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn={}&type=&otype=json'
        self.headers1 = {'host': 'api.bilibili.com',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
        self.headers2 = {'host': '',
                         'Origin': 'https://www.bilibili.com',
                         'Referer': 'https://www.bilibili.com/video/av{}',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

    def getCid(self, url):
        # 得到 cid
        data = requests.get(url, headers=self.headers1).json()
        detail = data['data'][0]
        cid = detail['cid']
        name = detail['part']
        duration = detail['duration']
        return cid, name, duration

    def getFlv(self, url):
        # 得到 flv
        data = requests.get(url, headers=self.headers1).json()
        durl = data['data']['durl'][0]
        size = durl['size']
        url = durl['url']
        length = durl['length']
        return length, size, url

    def download(self, url, filename='None.flv'):
        # 下载
        size = 0
        response = requests.get(url, headers=self.headers2, stream=True, verify=False)
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
            filename = os.path.join(self.output, filename)
            with open(filename, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    file.flush()
                    sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                    if size / content_size == 1:
                        print('\n')
        else:
            print('下载出错')

    def start(self, av):
        # 开始
        cid, name, duration = self.getCid(self.cid_url.format(av))
        print(cid,name,duration)
        length, size, flv = self.getFlv(self.flv_url.format(av, cid, self.qn))
        host = flv.split('/')[2]
        self.headers2['host'] = host
        filename = name.replace(' ', '_') + '.flv'
        print("name: {0} duration:{1}s".format(filename, duration))
        print(flv)
        self.download(flv, filename)


if __name__ == '__main__':
    bilibili = BilibiliCrawler(qn=80, output="download")
    avlist = ['91448364']
    for i in avlist:
        bilibili.start(av=i)