import redis

redis_config = {
            'host': '192.168.0.124',
            'port': 6379,
            'db': 1,
            'password': None,
        }
redis_client = redis.StrictRedis(**redis_config)
start_url = 'http://hotel.elong.com/huangshan/?tdsourcetag=s_pcqq_aiomsg'
redis_client.lpush('elong:start_urls', start_url)

# import requests
#
# header = {
#
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Cookie': 'xIka_2132_saltkey=f9IZ9CYV; xIka_2132_lastvisit=1569747417; UM_distinctid=16d7c73b7703b2-0b7482b610fc5c-67e153a-1fa400-16d7c73b771b6b; xIka_2132_forum_lastvisit_page=%7B%22fid%22%3A%22466%22%7D; xIka_2132_forum_lastvisit=D_570_1569751028D_466_1569752805; CNZZDATA30092183=cnzz_eid%3D731814808-1569747253-https%253A%252F%252Fbbs.feng.com%252F%26ntime%3D1569752653; xIka_2132_lastrequest=36d9sryMkV5UMIltvNP36OX35JrCKfuJJnJFWg8jsOwCT2LKO9fG; xIka_2132_viewid=tid_12488693; xIka_2132_guestcookieid=91ae9b13d2bf61d424289ff6a20deca8; xIka_2132_lastact=1569752838%09onlinetimaAjax.php%09',
# 'Host': 'bbs.feng.com',
# 'Referer': 'https://bbs.feng.com/read-htm-tid-12488693.html',
# 'Sec-Fetch-Mode': 'navigate',
# 'Sec-Fetch-Site': 'same-origin',
# 'Sec-Fetch-User': '?1',
# 'Upgrade-Insecure-Requests': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
#
# }
# url = 'https://bbs.feng.com/read-htm-tid-12488693.html'
# res = requests.get(url,headers=header).text
# print(res)
