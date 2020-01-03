from selenium import webdriver
import requests

# url = 'https://gz.58.com/huangyezonghe/?key=%E8%B4%B7%E6%AC%BE&final=1&searchtype=3&classpolicy=main_A,service_A,house_A,job_A,car_A,sale_A,huangyezonghe_B&tdsourcetag=s_pcqq_aiomsg&qq-pf-to=pcqq.group'
# browser = webdriver.Chrome()
# browser.get(url)
# a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# list = []
# for one in a:
#     list.append(one)
# print(list)




header = {
    # 'Referer': 'http://www.iheima.com/',
# 'Accept': 'application/json, text/plain, */*',
'Origin': 'https://es.aliexpress.com',
    'Referer': 'https://es.aliexpress.com/item/32726463724.html',
    # 'Cookie': '_WX=jsuchtk5ga1lvjkgram50b8t23; IDX_AD_SHOWED=d4da28225d098e1f9d5fc6273c0d254ab60f718478db39f18c1745f9e799e804a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22IDX_AD_SHOWED%22%3Bi%3A1%3Bb%3A1%3B%7D; _csrf=00d4abf7556fbd86ef30d02a5f7bd4fd6a71be770efae7c177201460386e7a95a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22V42xKFzcUn3CAKE4EyY1XTFtfHDwYoXy%22%3B%7D; DH_MM_ID=eznU711Kd7mIiDYIBHA7Ag==; Hm_lvt_9723485e19f163e8e518ca694e959cb9=1565161405; Hm_lpvt_9723485e19f163e8e518ca694e959cb9=1565161412',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    # 'X-Requested-With': 'XMLHttpRequest'
    # 'cookie': 'ali_apache_id=10.103.166.17.1565164479460.203431.1; xman_us_f=x_locale=es_ES&x_l=1; intl_locale=es_ES; aep_usuc_f=site=esp&c_tp=EUR&region=CN&b_locale=es_ES; xman_t=zFQRmIOX2sUX2h5vMZbS7+H7cCU0Rn/rzsvpFLbw/G5q8llLAj5GaITYwsSu9dVW; xman_f=8xJKvgfkGzNYHdR4KCR6tMFGz0kB71IbO8gDI0l+2+kMG2VvV04DZpsPMRt8Kl++X1hsF6MspGx/C3MLa7MWEHVxVOU135XUkbhPYpY7md8d/wb0PAsa4Q==; ali_apache_track=; ali_apache_tracktmp=; acs_usuc_t=acs_rt=92996b21906b44019be05df76903418a&x_csrf=6y71pquy0b0d; cna=wHHRFZ0LIHICAdoT3qWQ8eI0; XSRF-TOKEN=15a5a136-bfd1-4812-901d-662ac8b2620e; intl_common_forever=hJorbWYzfxMWgxjAhUJHQsLI+YHxu3/01o1I1Z++6AnWveeJ24s45Q==; _bl_uid=jzjUnz2k0ybyvbi4gqhmuRbg4nk8; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932726463724; _uab_collina=156516448129554237272833; _m_h5_tk=3f12ea074a21b7fff94ce190a1c19c39_1565173481195; _m_h5_tk_enc=5f6972a3d03cf7c90a0a13002b26cab2; _ga=GA1.2.1527318272.1565164482; _gid=GA1.2.521001888.1565164482; _gat=1; JSESSIONID=1AC0281F2D86E913A90F6341DEA71B87; l=cBOq56dlqRB0XRFoBOfN5uI8aV7OXIRb8sPzw4_G8ICPOj1JueXfWZFw178vCnGVLs3pJ35GDcqQBzLuNy4ECHKYyAELlFnO.; isg=BAcHZ1RkFtSm25JYSuQLjqhclrsRpNuTw8tXKNn03RahSCYK4NlgP2ZC6kizoLNm'
}

url = 'https://moduleanalysis.aliexpress.com/item/desc/module/analysis.json?moduleIds=24591988,22619821&adminAccountId=221558572'
res = requests.get(url,headers=header)
print(res.text)
# for i in range(100,150):
#     url = 'http://www.iheima.com/?page={}&pagesize=20'.format(i)
#     res = requests.get(url,headers=header)
#     json_mes = res.json()
#     if json_mes.get('contents'):
#         print(i)
#         print(len(json_mes.get('contents')))
#         pass
#     else:
#         print(i)
#         print('结束')
#         print(len(json_mes.get('contents')))
#         break