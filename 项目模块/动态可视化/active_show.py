import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML


df = pd.read_csv('111.csv')
current_year = 1996
dff = (df[df['year'].eq(current_year)].sort_values(by='value', ascending=True).head(10))  # 读出1996年份的数据并按 ’value‘ 从小到大排序
# fig, ax = plt.subplots(figsize=(15, 8))
colors = dict(zip(
    ['North America', 'Asia', 'Middle East'],
    ['#adb0ff', '#ffb3ff', '#90d595']
))  # 指定各个地区对应的颜色 生成字典
group_lk = df.set_index('name')['group'].to_dict()  # 让名字和分组对应生成字典

def draw_barchart(year):
    dff = df[df['year'].eq(year)].sort_values(by='value', ascending=True).tail(10)  # 选取满足条件的后10行
    ax.clear()
    ax.barh(dff['name'], dff['value'], color=[colors[group_lk[x]] for x in dff['name']])  # 获取数据中每个分钟对应的颜色 并设置
    dx = dff['value'].max() / 200
    for i, (value, name) in enumerate(zip(dff['value'], dff['name'])):  # 配置数据及显示的格式
        ax.text(value - dx, i, name, size=14, weight=600, ha='right', va='bottom')
        ax.text(value - dx, i - .25, group_lk[name], size=10, color='#444444', ha='right',
                va='baseline')  # Asia: 组名  i-.25'为坐标往下偏移  ha='' 为  显示的位置
        ax.text(value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center')  # value+dx’为坐标向右偏移
    # ... polished styles
    ax.text(1.1, 0.4, year, color='#777777', transform=ax.transAxes, size=46, ha='right',
            weight=800)  # 设置年份的显示位置，颜色，大小，字体粗度
    ax.text(0, 1.06, 'Population (thousands)', transform=ax.transAxes, size=12,
            color='#777777')  # 这里的,transform=axs.transAxes就是轴坐标，大概意思就是左边距离横坐标轴长的0.1倍，下面距离纵坐标轴的0.90倍，如果不写的话默认就是data坐标，即0.1代表横轴的0.1个单位，即坐标点
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))  # x 轴坐标参数 改为 19,751 格式
    ax.xaxis.set_ticks_position('top')  # x 轴坐标参数 x轴显示到上方
    ax.tick_params(axis='x', colors='#777777', labelsize=12)  # x 轴坐标参数 颜色，大小
    ax.set_yticks([])  # 不显示y 轴
    ax.margins(0, 0.01)  # 缩放坐标
    ax.grid(which='major', axis='x', linestyle='-')  # 设置坐标竖线
    ax.set_axisbelow(True)  # 设置坐标为背景
    ax.text(0, 1.12, 'The most populous cities in the world from 1500 to 2000',
            transform=ax.transAxes, size=24, weight=600, ha='left')  # 加标题
    #     ax.text(1, 0, 'by QIML', transform=ax.transAxes, ha='right',
    #             color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)

# draw_barchart(1600)
#生成动态图
fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(1790, 1800))
HTML(animator.to_jshtml())
# plt.show()