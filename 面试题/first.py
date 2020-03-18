import tushare as ts
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#第一题
class GetRetracement():
    """计算 000001.SZ 股票的 2017-2019 的每月回撤率"""
    def getdata(self):
        pro = ts.pro_api('0bb0b361e40272ca91a4bf0e8a2496a2d8d8e65fdefbf611daa2d988')
        # 月数据
        df = pro.monthly(ts_code='000001.SZ', start_date='20170101', end_date='20190101', fields='ts_code,trade_date,open,high,low,close,vol,amount')
        # 天数据
        # df = pro.daily(ts_code='000001.SZ', start_date='20200317', end_date='20200318')
        print(df)

        # df.to_excel('2017-2019data.xlsx', index=False)

    def count_data(self):
        """算最大回撤率"""
        df = pd.read_excel('2017-2019data.xlsx')
        df['retracement'] = (df['high']-df['low'])/df['high']
        df['retracement_rate'] = df['retracement'].apply(lambda x: format(x, '.2%'))
        # print(df) #数据
        print('最大回撤为：' ,format(df['retracement'].max(),'.2%'))
        self.write_data(50.0,df,'2017-2019直方图.png')
        df.to_excel('2017-2019data_after.xlsx',index=False)

    def write_data(self,len,data,name='直方图.png'):
        """绘制直方图"""
        plt.figure(figsize=(len, 10.0))
        df = data
        sns.barplot(x='trade_date', y="retracement", data=df)
        plt.savefig(name)
        plt.show()



#第二题
class FinancialCrisis():
    """查阅相关资料，大概可得到金融危机大概有2008年1-9月的‘次贷危机’，2015年6-10月的‘股灾’2020年1-2月的‘疫情’"""

    def getdata(self):
        """获取数据，把时间稍扩大一点"""
        pro = ts.pro_api('0bb0b361e40272ca91a4bf0e8a2496a2d8d8e65fdefbf611daa2d988')
        # 月数据
        while True:
            try:
                cd_df = pro.monthly(ts_code='000001.SZ', start_date='20080101', end_date='20081001',
                                 fields='ts_code,trade_date,open,high,low,close,vol,amount')
                gz_df = pro.monthly(ts_code='000001.SZ', start_date='20150601', end_date='20151101',
                                 fields='ts_code,trade_date,open,high,low,close,vol,amount')
                yq_df = pro.monthly(ts_code='000001.SZ', start_date='20200101', end_date='20200301',
                                 fields='ts_code,trade_date,open,high,low,close,vol,amount')
                break
            except Exception as e:
                print(e)


        df = pd.concat([cd_df, gz_df, yq_df])
        # 天数据
        # df = pro.daily(ts_code='000001.SZ', start_date='20200317', end_date='20200318')
        print(df)
        # df.to_excel('FinancialCrisis_data.xlsx', index=False)

    def count_data(self):
        """算各个时间段的最大回撤率"""
        df = pd.read_excel('FinancialCrisis_data.xlsx')
        df['retracement'] = (df['high'] - df['low']) / df['high']
        df['retracement_rate'] = df['retracement'].apply(lambda x: format(x, '.2%'))
        #分开各个部分
        title = ['2018_1-9','2015_6-10','2020_1-2']
        re_list = []
        cd_df =  df[df['trade_date']<20090101]  #2008
        re_list.append((cd_df['high'].max()-cd_df['low'].min())/cd_df['high'].max())
        # print((cd_df['high'].max()-cd_df['low'].min())/cd_df['high'].max())
        gz_df = df[(df['trade_date']<20160101) & (20140101 <df['trade_date'])]   #2015
        re_list.append((gz_df['high'].max() - gz_df['low'].min()) / gz_df['high'].max())
        yq_df =  df[df['trade_date']>20191201] #2020
        re_list.append((yq_df['high'].max() - yq_df['low'].min()) / yq_df['high'].max())
        data = pd.DataFrame(data = {'trade_date':title,'retracement':re_list})
        print('2018年1-9月，2015年6-10月，2020年1-2月，回撤率分别为：','，'.join([format(x, '.2%') for x in re_list]) )
        data['retracement_rate'] = data['retracement'].apply(lambda x: format(x, '.2%')) #算百分比
        # print(data) #数据
        self.write_data(5.0,data,'危机直方图_按时间段.png') #保存图片
        #按月统计
        df['retracement'] = (df['high'] - df['low']) / df['high']
        df['retracement_rate'] = df['retracement'].apply(lambda x: format(x, '.2%'))
        print(df)
        self.write_data(15.0,df,'危机直方图_按月.png')

    def write_data(self,len,data,name='直方图.png'):
        """绘制直方图"""
        plt.figure(figsize=(len, 5.0))
        df = data
        sns.barplot(x='trade_date', y="retracement", data=df)
        plt.savefig(name)
        plt.show()

if __name__ == '__main__':
    # getdata()
    a = GetRetracement()
    a.count_data()
    a = FinancialCrisis()
    a.count_data()