import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties


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
                print(download_path)
                print(self.all_download_path)
                download_path = self.all_download_path
            plt.savefig(download_path)
            print('保存成功{}'.format(download_path))
        plt.show()


if __name__ == '__main__':
    # 数据准备（蜘蛛图）
    labels = np.array([u" 推进 ", "KDA", u" 生存 ", u" 团战 ", u" 发育 ", u" 输出 "])
    stats = [20, 50, 95, 47, 56, 88]
    a = MatplotChart()
    a.radar_chart(labels, stats, isdownload=True)
