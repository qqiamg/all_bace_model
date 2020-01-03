# -*- coding: utf-8 -*-
# __author__ = 'WTL'
# __blog__ = 'www.whcblog.com'

import requests


from YDMHTTPDemo import YDMHttp
from lxml import etree


def get_code():
    filename = '1.jpg'
    codetype = 4006
    timeout = 25
    username = 'ace892694285'
    password = 'Ys6688'
    appid = 1
    appkey = '22cc5376925e9387a23cf797cb9ba745'
    yundama = YDMHttp(username, password, appid, appkey)
    cid, result = yundama.decode(filename, codetype, timeout)
    print(result)
    return result


if __name__ == '__main__':
    get_code()
