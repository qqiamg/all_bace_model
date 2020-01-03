import time
import datetime

"""转换时间戳到时间"""
# 使用time
timeStamp = 1381419600
timeArray = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print(otherStyleTime)  # 2013--10--10 23:40:00
# 使用datetime
timeStamp = 1381419600
dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
print(otherStyleTime)  # 2013--10--10 15:40:00

"""转换时间到时间戳"""
# 字符类型的时间
tss1 = '2013-10-10 23:40:00'
# 转为时间数组
timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
print(timeArray)
# timeArray可以调用tm_year等
print(timeArray.tm_year)  # 2013
# 转为时间戳
timeStamp = int(time.mktime(timeArray))
print(timeStamp)  # 1381419600

"""获取当前时间"""
t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(t)
