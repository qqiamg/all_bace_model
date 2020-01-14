import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
import scipy.stats as sci


class MatplotChart(object):
    """各类表"""

    def __init__(self):
        self.all_download_path = 'file.jpg'

    def radar_chart(self, title, data, isdownload=False, download_path=None):
        """
        画雷达图
        :param title: 标题（list）
        :param data: 数据大小(list)
        :param isdownload: 是否下载
        :param download_path: 下载名称
        :return:
        """
        labels = np.array(title)
        stats = data
        download_path = download_path
        # 画图数据准备，角度、状态值
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)  # 从0 开始到2π 等分6个
        stats = np.concatenate((stats, [stats[0]]))  # 拼接
        angles = np.concatenate((angles, [angles[0]]))
        # 用 Matplotlib 画蜘蛛图
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, stats, 'o-', linewidth=2)  # 传入弧度 和长度
        ax.fill(angles, stats, alpha=0.25)  # 设置透明度
        # 设置中文字体
        font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)
        ax.set_thetagrids(angles * 180 / np.pi, labels, FontProperties=font)
        if isdownload:  # 要放到 show() 前
            if download_path is None:
                download_path = self.all_download_path
            else:  # 判断路径是否存在，不存在先新建
                z = download_path.count("/")
                if z <= 1:
                    pass
                else:
                    file_d = download_path.replace(f"{download_path.split('/')[-1]}", '')
                    if not os.path.exists(file_d):  # 新建文件夹
                        os.makedirs(file_d)
            plt.savefig(download_path)
            print('保存成功{}'.format(download_path))
        plt.show()

    def scatter_distribution_chart(self, x_name, y_name, data, isdownload=False, download_path=None, kind='scatter'):
        """
        画散点分布图(传入dataframe)
        :param x_name: x轴的数据名称
        :param y_name: y轴的数据名称
        :param data: 数据
        :param isdownload: 是否下载
        :param download_path: 下载路径
        :param kind: 散点图类型 “scatter” | “reg” | “resid” | “kde” | “hex”
        :return:
        """
        plt.figure(figsize=(15.0, 10.0))
        if kind == 'kde':
            g = sns.jointplot(x=x_name, y=y_name, data=data, height=8, kind=kind, stat_func=sci.pearsonr)
            g.plot_joint(plt.scatter, c='w', s=30, linewidth=1, marker='+')
        else:
            sns.jointplot(x=x_name, y=y_name, data=data, height=8, marginal_kws=dict(bins=15, rug=True), kind=kind,
                          stat_func=sci.pearsonr)
        if isdownload:  # 要放到 show() 前
            if download_path is None:
                download_path = self.all_download_path
            else:  # 判断路径是否存在，不存在先新建
                z = download_path.count("/")
                if z <= 1:
                    pass
                else:
                    file_d = download_path.replace(f"{download_path.split('/')[-1]}", '')
                    if not os.path.exists(file_d):  # 新建文件夹
                        os.makedirs(file_d)
            plt.savefig(download_path)
            print('保存成功{}'.format(download_path))
        plt.show()

    def level_scatter_chart(self, x_name, y_name, data, isdownload=False, download_path=None):
        plt.figure(figsize=(15.0, 10.0))
        g = sns.JointGrid(x=x_name, y=y_name, data=data)
        g = g.plot_joint(plt.scatter, color='g', s=40, edgecolor='white', alpha=.5)  # 绘制散点图
        plt.grid(linestyle='--')  # 网格
        g.plot_marginals(sns.distplot, kde=True, color='g')
        if isdownload:  # 要放到 show() 前
            if download_path is None:
                download_path = self.all_download_path
            else:  # 判断路径是否存在，不存在先新建
                z = download_path.count("/")
                if z <= 1:
                    pass
                else:
                    file_d = download_path.replace(f"{download_path.split('/')[-1]}", '')
                    if not os.path.exists(file_d):  # 新建文件夹
                        os.makedirs(file_d)
            plt.savefig(download_path)
            print('保存成功{}'.format(download_path))
        plt.show()

if __name__ == '__main__':
    """蜘蛛图"""
    # labels = np.array([u" 推进 ", "KDA", u" 生存 ", u" 团战 ", u" 发育 ", u" 输出 "])
    # stats = [20, 50, 95, 47, 56, 88]
    # a = MatplotChart()
    # a.radar_chart(labels, stats, isdownload=True)
    """散点分布图"""
    # tips = sns.load_dataset("tips")  # s数据源
    # a = MatplotChart()
    # a.scatter_distribution_chart('total_bill', 'tip', tips, kind='kde')
    """散点，柱状，曲线图"""
    tips = sns.load_dataset("tips")  # s数据源
    a = MatplotChart()
    a.level_scatter_chart('total_bill', 'tip', tips)
