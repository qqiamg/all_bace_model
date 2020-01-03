import requests


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


if __name__ == '__main__':
    ###使用例子###

    # 代理隧道验证信息
    proxyUser = "H78E038C914N59UD"
    proxyPass = "89FAFE4359C271B7"
    res = requests.get('htttps://www.baidu.com', proxies=proxies_api(proxyUser, proxyPass))
