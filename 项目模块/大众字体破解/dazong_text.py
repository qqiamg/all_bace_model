import requests

_default_headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Cookie': '_lxsdk_cuid=16d48f06c50c8-0785cf932c338-67e1b3f-1fa400-16d48f06c50c8; _lxsdk=16d48f06c50c8-0785cf932c338-67e1b3f-1fa400-16d48f06c50c8; _hc.v=4632807d-b208-a001-a974-d0249b265040.1568886779; s_ViewType=10; ua=dpuser_4297777734; ctu=f99ecd3aee349826af7a81577860e8282d1363f592023a38a178b6e9d91abfe7; uamo=15112001518; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; cy=499; cye=anguo; _lxsdk_s=16e40319573-6f-930-581%7C%7C385',
    'Host': 'www.dianping.com',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}

url = 'https://www.dianping.com/citylist'
res = requests.get(url, headers=_default_headers)
res.encoding = 'utf-8'
print(res.text)
