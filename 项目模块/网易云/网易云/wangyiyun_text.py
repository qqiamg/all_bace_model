from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pyquery import PyQuery
import requests
import os

#********************************#
# 程序功能：                      #
#      通过用户输入歌曲名字和歌手  #
#  名，获取歌曲的ID值，进行下载，  #
#  可下载会员的歌曲。             #
#                               #
#*******************************#




download_url = "http://music.163.com/song/media/outer/url?id="



def new_browser(target_name):
    #####################################
    #                                   #
    #功能：获取所需爬取的歌曲的源码并返回  #
    #                                   #
    #####################################

    #初始化，并赋值给对象
    # 创建chrome参数对象
    opt = webdriver.ChromeOptions()
    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    opt.set_headless()
    # 创建chrome无界面对象
    browser = webdriver.Chrome(options=opt)
    browser.implicitly_wait(10)                     #隐性等待10s
    browser.get('https://music.163.com/#/search')   #访问url



    # 使用css选择器 获取 class值为service-bd 的代码里的所有 li 节点
    # 参考链接：http://www.w3school.com.cn/cssref/css_selectors.asp
    # ############################################################

    time.sleep(0.5)
    browser.switch_to.frame('g_iframe')
    input = browser.find_element_by_xpath('//*[@id="m-search-input"]')

    input.send_keys(target_name)       #输入文字
    #time.sleep(1)
    input.send_keys(Keys.ENTER)
    time.sleep(0.5)

    text = browser.page_source
    res = PyQuery(text)
    browser.close()
    return res


class GetMessage():
    #####################################
    #                                   #
    #功能：获取所需爬取的歌曲各类信息      #
    #                                   #
    #####################################
    def __init__(self, res):
        self.res = res

    def get_id(self):
        #获取歌曲id
        id_find = self.res('.srchsongst .item .td .hd ') #获取song_id 所在的父节点
        id_get = id_find.children()                      #获取所在的节点
        song_id = id_get.attr('data-res-id')             #获取id值
        print('\n获取的歌曲ID： ' + song_id)
        return song_id

    def get_name(self):
        #获取歌名
        name_find =self.res('.srchsongst .item .td.w0 .sn .text')
        name_get = name_find.children().children()
        song_name = name_get.attr('title')
        print('获取的歌名： ' + song_name)
        return song_name

    def get_singer(self):
        #获取歌手
        singer_find =self.res('.srchsongst .item .td.w1 .text')
        singer_get = singer_find.children()
        singer_name = singer_get[0].text                #获取第一位的名字
        print('获取的歌手： ' + singer_name)
        return singer_name
            # browser.close()

def download_song(ID, name, singer):
    """运用requests库下载"""
    new_name = name + '_' +singer +'.mp3'
    download = download_url + ID
    UA1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_14)'
    UA2 = 'AppleWebKit/537.36(KHTML, like Gecko)Chrome/52.0.2743.166 Safari/537.36'
    headers = {
        'User-Agent': UA1+UA2,
    }
    print("下载中")
    r = requests.get(download, headers=headers)
    if not os.path.exists('music'):
        os.mkdir('music')
    local = 'music/' + new_name
    #判断是否已下载
    if not os.path.exists(local):
        with open(local, 'wb') as f:
            #下载
            f.write(r.content)
        print('下载完成')
    else:
        print('已经下载过本歌曲')

shu = 0

def main():
    while True:
        print('(退出请输入"q")')
        music_name = input('请输入歌名：')
        if music_name == 'q':
            break
        singer = input("请输入歌手：")
        if singer == 'q':
            break
        target_name = music_name + ' ' + singer
        global shu
        shu += 1
        print('\n第' + str(shu) + '首歌下载：')
        print('获取数据中...')
        Res = new_browser(target_name)
        mes = GetMessage(Res)
        ID = mes.get_id()
        name = mes.get_name()
        Singer = mes.get_singer()
        download_song(ID, name, Singer)


if __name__ == '__main__':
    main()

