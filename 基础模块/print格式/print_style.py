from tqdm import tqdm
import time

page_count = 60
"""
两种不刷新的答应进度
"""
# 一、用封装好的库
for page in tqdm(range(1, page_count + 1), desc='Progress'):
    time.sleep(1)

# # 二、用print()语句的写法实现， \r 回到第一行，end='' 不换行
# for i in range(100):
#     print('\r第%d页' % i, end='')
#     time.sleep(1)
