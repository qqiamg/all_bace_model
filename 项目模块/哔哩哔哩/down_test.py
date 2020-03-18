import requests
import sys
def down():
    # url = 'https://cn-sh-cc-bcache-01.bilivideo.com/upgcxcode/09/56/156155609/156155609-1-16.mp4?e=ig8euxZM2rNcNbKBhwdVtWKBhwdVNEVEuCIv29hEn0lqXg8Y2ENvNCImNEVEUJ1miI7MT96fqj3E9r1qNCNEtodEuxTEtodE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==&uipk=5&nbs=1&deadline=1583603541&gen=playurl&os=bcache&oi=3753953192&trid=35153682d5884a16aff0bab07f276dd8u&platform=pc&upsig=18c0499d4e6ed68c86527e3e86ffcfb9&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=10789807&logo=40000000'
    # url = 'https://cn-gdfs2-cc-bcache-03.bilivideo.com/upgcxcode/09/56/156155609/156155609-1-64.flv?e=ig8euxZM2rNcNbRghwdVhoM1hbdVhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNo8g2ENvNo8i8o859r1qXg8xNEVE5XREto8GuFGv2U7SuxI72X6fTr859r1qXg8gNEVE5XREto8z5JZC2X2gkX5L5F1eTX1jkXlsTXHeux_f2o859IB_&uipk=5&nbs=1&deadline=1583604600&gen=playurl&os=bcache&oi=3753953192&trid=f1e8bed359bd4a069731889846fc60feu&platform=pc&upsig=8bc23fc4ae7dc00e7c5f23b64482c535&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=10789807&logo=80000000'
    headers = {'host': '',
                     'Origin': 'https://www.bilibili.com',
                     'Referer': 'https://www.bilibili.com/video/av123456',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

    res = requests.get('https://api.bilibili.com/x/player/playurl?avid=66476652&cid=115287880&fnval=1')
    json_msg = res.json()
    durl = json_msg['data']['durl'][0]
    url = durl['url']
    print(url)
    host = url.split('/')[2]
    print(host)
    headers['host'] = host
    size = 0
    ress = requests.get(url, headers=headers,timeout=10, stream=True, verify=False) #添加下载参数 stream=True 文件过大需要添加防止内存过大
    content_size = int(ress.headers['content-length'])
    file = open("1.mp4", "wb")
    for data in ress.iter_content(chunk_size=1024):
        file.write(data)
        size += len(data)
        file.flush()
        # print(int(size / content_size * 100))
        if int(size / content_size * 100)%10 == 0:
            print('\r[下载进度]:%.2f%%' % float(size / content_size * 100), end='')
        # print('\r[下载进度]:%.2f%%' % float(size / content_size * 100), end='')
        #     sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
    print(ress)
# size = 10
# content_size = 11
# if content_size%size==0:
#     print(111)
# print('host')
# print('\r[下载进度]:%.2f%%' % float(size / content_size * 100), end='')
# print('\r[下载进度]:%.2f%%' % float(size / content_size * 101), end='')
# sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
# sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 10) + '\r')
down()