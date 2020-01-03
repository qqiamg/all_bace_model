from selenium import webdriver
import random
import pandas as pd

# url = 'https://detail.hipac.cn/item.html?itemId=37254&rp=2.4.130.0.4.k3p7qcej1'
data_name = ['kaiachi', 'cairo', 'beijing', 'New York', 'osaka', 'shanghai']
next_ = ['Asia', 'Middle East', 'Asia', 'North America', 'Asia', 'Asia']
all_data = []
num = [16070, 15400, 14080, 11601, 17400, 14080]
for i in range(500):
    for j, one_data in enumerate(data_name):
        zz = num[j] + random.uniform(-50, 100)
        lins_list = [one_data, next_[j], 1500 + i, round(zz, 2)]
        all_data.append(lins_list)
        print(lins_list)
        num[j] = round(zz, 2)

z_df = pd.DataFrame(data=all_data, columns=['name', 'group', 'year', 'value'])
z_df.to_csv('111.csv', index=False)

# df = pd.read_csv('111.csv')
# df.head(5)
# df['year'].eq(1688)
# print(df)
