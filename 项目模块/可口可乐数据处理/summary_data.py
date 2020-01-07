import pandas as pd
import time
import datetime

"""11.14问题：
    1、百分比的转换。
    2、百分比转换的前两项是求平均
"""


###汇总所有子表到汇总表中###

class SummaryData(object):
    def __init__(self):
        self.summary_file = '测试设置表.xlsx'
        self.table_row_list = []  # 存储对应获取表的列
        self.table_nameid_list = []  # 存储需要读取的excel 文件(ou)
        self.table_nameid_banner_list = []  # 存储需要读取的excel 文件(banner)
        self.bybanner_path_list = []  # 用于存放byBanner 的文件路径
        self.byou_path_list = []  # 用于存放byOU 的文件路径

    def get_table_row(self):
        """获取汇总表的所有对应行数据和对应文件"""
        df = pd.read_excel(self.summary_file, sheet_name='TableCopy')  # 可以通过sheet_name来指定读取的表单
        all_title_name = df.columns.values  # 获取所有表头
        table_row = df[all_title_name[:6]]
        for i in range(len(table_row)):
            lins_list = list(table_row.iloc[i])
            for j, one_data in enumerate(lins_list):
                if str(one_data) == 'nan':
                    lins_list[j] = ''
            self.table_row_list.append(lins_list)
        # print(self.table_row_list)

        table_nameid_title = all_title_name[10:]
        table_nameid = df[table_nameid_title]
        for j, one_src in enumerate(table_nameid):
            lins_list = list(table_nameid[one_src].dropna().values)
            lins_list.insert(0, table_nameid_title[j])
            self.table_nameid_list.append(lins_list)
            self.table_nameid_banner_list.append([table_nameid_title[j]])
        print(self.table_nameid_list)

    def get_indexfile_path(self):
        """获取对应文件对应的路径"""
        # byBanner
        byBanner_df = pd.read_excel(self.summary_file, sheet_name='bybanner')  # 获取表byBanner 的数据
        all_title_name = byBanner_df.columns.values  # 获取所有表头
        table_row = byBanner_df[all_title_name[:5]]
        # 生成表对应的id
        max_row = list(table_row.iloc[len(table_row) - 1])[-1]
        for one_table in self.table_nameid_banner_list:
            lins_list = [x for x in range(1, max_row + 1)]
            for i in lins_list:
                one_table.append(i)
        for i in range(len(table_row)):
            lins_list = list(table_row.iloc[i])
            for j, one_data in enumerate(lins_list):
                if str(one_data) == 'nan':
                    lins_list[j] = ''
            self.bybanner_path_list.append(lins_list)

        # print(self.bybanner_path_list)
        # byOU
        byOU_df = pd.read_excel(self.summary_file, sheet_name='byou')  # 获取表byOU 的数据
        all_title_name = byOU_df.columns.values  # 获取所有表头
        table_row = byOU_df[all_title_name[:4]]
        for i in range(len(table_row)):
            lins_list = list(table_row.iloc[i])
            for j, one_data in enumerate(lins_list):
                if str(one_data) == 'nan':
                    lins_list[j] = ''
            self.byou_path_list.append(lins_list)
        # print(self.byou_path_list)

    def get_hs_mini(self, table):
        """处理Availability.HS.src 和 Availability.Mini.src"""
        net_list = []
        t2 = list(table[0])
        # print(t2)
        for j, i in enumerate(t2):  # 算是哪里切割
            # print(i)
            try:
                if 'NET' in i:
                    print(j, i)
                    net_list.append(j)
            except:
                pass
        all_title_name = table.columns.values  # 获取所有表头
        print(len(all_title_name))
        table.fillna(value=0, inplace=True)  # 替换空值为0
        for i in range(1, len(all_title_name) - 1):
            print(i)
            all_dd = []
            print('NET - Availability-Sparkling / 汽水铺货率')
            # print(net_list)
            first_net = table[net_list[0] + 1:net_list[1]]
            # print(first_net)
            sparkling = round(first_net[i].mean(), 4)
            print(sparkling)
            print('NET - Availability-STILL / 非汽水铺货率')
            second_net = table[net_list[1] + 1:len(t2) + 1]
            # print(second_net)
            STILL = round(second_net[i].mean(), 4)
            print(STILL)
            all_dd.append(first_net)
            all_dd.append(second_net)
            lins_df = pd.concat(all_dd, ignore_index=True)
            # print(lins_df)
            all_average = round(lins_df[i].mean(), 4)
            print(all_average)
            table.iloc[net_list[0], i] = sparkling
            table.iloc[net_list[1], i] = STILL
            table.iloc[2, i] = all_average
            # print(t)
        print(table)
        return table
        # t.to_excel('dddddddd.xlsx')

    def get_each_row_mes_ou(self):
        """获取组合表每行的数据(ou:生成)"""
        # ou的路径
        byou_nameid_path_list = []
        # print(self.table_nameid_list)
        # print(self.byou_path_list)
        for one_src in self.table_nameid_list:
            lins_list = []
            lins_list.append(one_src[0])
            # print(lins_list)
            for one_id in one_src[1:]:
                for one_uo_path in self.byou_path_list:
                    if int(one_id) == int(one_uo_path[3]):
                        id_path = [one_id, one_uo_path[0]]
                        lins_list.append(id_path)
            byou_nameid_path_list.append(lins_list)
        # print(byou_nameid_path_list)  # 生成带id和路径的源文件
        t = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        print('开始：', t)
        writer = pd.ExcelWriter("byouSS.xlsx")
        for one_src in byou_nameid_path_list:  # 循环每一个需生成的 src文件
            src_name = one_src[0]
            table_id = 1
            df_list = []
            for one_excel_name in one_src[1:]:  # 循环每一个子excel 文件
                # print(one_excel_name)
                print(table_id)
                lins_df_list = []
                for j, one_table_line in enumerate(self.table_row_list):  # 循环某个表格的每行数据
                    # 1、成byOU 的总表
                    # print(one_table_line)
                    file_name = one_table_line[0]  # 保存的目标src 文件名
                    if src_name == file_name:  # 匹配对应 的文件路径
                        # if src_name == 'Availability.HS.src'
                        ou_src_sheet = one_table_line[2]  # ou 数据的原目标sheet
                        try:
                            start_row = int(one_table_line[4])  # 开始行数
                        except:
                            start_row = ''
                        try:
                            end_row = int(one_table_line[5])  # 结束行数
                        except:
                            end_row = ''

                        ou_path = one_excel_name[1]  # 源文件路径
                        tid = one_excel_name[0]
                        type = str(one_table_line[1])  # 类型
                        if type == '%':
                            ou_path = ou_path.replace('Abs', '%')
                            print([file_name, ou_src_sheet, start_row, end_row, ou_path])
                            lins_df = pd.read_excel(ou_path, sheet_name=ou_src_sheet, header=None)
                            if start_row and end_row:
                                # all_title_name = len(lins_df.columns.values)
                                t2 = lins_df[start_row - 1:end_row]
                                tx = t2.iloc[:, 1:] / 100
                                t2.iloc[:, 1:] = tx
                                # print(t2)
                                t2['tid'] = tid
                                lins_df_list.append(t2)
                            else:
                                lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                        else:
                            print([file_name, ou_src_sheet, start_row, end_row, ou_path])
                            lins_df = pd.read_excel(ou_path, sheet_name=ou_src_sheet, header=None)
                            if start_row and end_row:
                                t2 = lins_df[start_row - 1:end_row]
                                t2['tid'] = tid
                                lins_df_list.append(t2)
                            else:
                                lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                        # if j == len(self.table_row_list):#(11.14 忘记用来改吗的了)
                        #     pass
                    else:
                        pass  # 清空表计数
                lins_df_ = pd.concat(lins_df_list, ignore_index=True)  # 替换空值为0
                lins_df_.fillna(value=0, inplace=True)  # 替换空值为0
                if src_name == "Availability.HS.src" or src_name == "Availability.Mini.src":
                    lins_df = self.get_hs_mini(lins_df_)
                else:
                    lins_df = lins_df_
                df_list.append(lins_df)
                df_list.append(pd.DataFrame([[]]))
                table_id += 1
            df1 = pd.concat(df_list, ignore_index=True)
            # print(df1)
            df1.to_excel(writer, index=False, sheet_name=src_name)
        t = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        print('结束：', t)
        writer.save()
        writer.close()

    def get_each_row_mes_banner(self):
        """获取组合表每行的数据(banner:生成)"""
        # ou的路径
        byou_nameid_path_list = []
        # print(self.table_nameid_list)
        # print(self.byou_path_list)
        for one_src in self.table_nameid_banner_list:
            lins_list = []
            lins_list.append(one_src[0])
            print(lins_list)
            for one_id in one_src[1:]:
                # print(one_id)
                for one_uo_path in self.bybanner_path_list:
                    # print(one_uo_path)
                    if int(one_id) == int(one_uo_path[4]):
                        id_path = [one_id, one_uo_path[0]]
                        lins_list.append(id_path)
            byou_nameid_path_list.append(lins_list)
        # print(byou_nameid_path_list)  # 生成带id和路径的源文件
        t = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        print('开始：', t)
        writer = pd.ExcelWriter("bybannerSS.xlsx")
        for one_src in byou_nameid_path_list:  # 循环每一个需生成的 src文件
            src_name = one_src[0]
            table_id = 1
            df_list = []
            for one_excel_name in one_src[1:]:  # 循环每一个子excel 文件
                # print(one_excel_name)
                print(table_id)
                lins_df_list = []
                for j, one_table_line in enumerate(self.table_row_list):  # 循环某个表格的每行数据
                    # 1、成byOU 的总表
                    # print(one_table_line)
                    file_name = one_table_line[0]  # 保存的目标src 文件名
                    if src_name == file_name:  # 匹配对应 的文件路径
                        # if src_name == 'Availability.HS.src'
                        ou_src_sheet = one_table_line[3]  # ou 数据的原目标sheet
                        try:
                            start_row = int(one_table_line[4])  # 开始行数
                        except:
                            start_row = ''
                        try:
                            end_row = int(one_table_line[5])  # 结束行数
                        except:
                            end_row = ''

                        ou_path = one_excel_name[1]  # 源文件路径
                        tid = one_excel_name[0]
                        type = str(one_table_line[1])  # 类型
                        if type == '%':
                            ou_path = ou_path.replace('Abs', '%')
                            print([file_name, ou_src_sheet, start_row, end_row, ou_path])
                            try:
                                lins_df = pd.read_excel(ou_path, sheet_name=ou_src_sheet, header=None)
                                if start_row and end_row:
                                    # all_title_name = len(lins_df.columns.values)
                                    t2 = lins_df[start_row - 1:end_row]
                                    tx = t2.iloc[:, 1:] / 100
                                    t2.iloc[:, 1:] = tx
                                    # print(t2)
                                    t2['tid'] = tid
                                    lins_df_list.append(t2)
                                else:
                                    lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                            except:
                                if start_row and end_row:
                                    for i in range(int(end_row - start_row) + 1):  # 添加对应的空行
                                        lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                                else:
                                    lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                        else:
                            print([file_name, ou_src_sheet, start_row, end_row, ou_path])
                            try:
                                lins_df = pd.read_excel(ou_path, sheet_name=ou_src_sheet, header=None)
                                if start_row and end_row:
                                    t2 = lins_df[start_row - 1:end_row]
                                    t2['tid'] = tid
                                    lins_df_list.append(t2)
                                else:
                                    lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                            except:
                                if start_row and end_row:
                                    for i in range(int(end_row - start_row) + 1):  # 添加对应的空行
                                        lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                                else:
                                    lins_df_list.append(pd.DataFrame([[tid]], columns=['tid']))
                        # if j == len(self.table_row_list):#(11.14 忘记用来干嘛的了)
                        #     pass
                    else:
                        pass  # 清空表计数
                lins_df_ = pd.concat(lins_df_list, ignore_index=True)  # 替换空值为0
                lins_df_.fillna(value=0, inplace=True)  # 替换空值为0
                if src_name == "Availability.HS.src" or src_name == "Availability.Mini.src":
                    lins_df = self.get_hs_mini(lins_df_)
                else:
                    lins_df = lins_df_
                df_list.append(lins_df)
                df_list.append(pd.DataFrame([[]]))
                table_id += 1
            df1 = pd.concat(df_list, ignore_index=True)
            # print(df1)
            df1.to_excel(writer, index=False, sheet_name=src_name)
        t = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        print('结束：', t)
        writer.save()
        writer.close()

    def run(self):
        """生成汇总表"""
        self.get_table_row()
        self.get_indexfile_path()
        self.get_each_row_mes_banner()  # banner 表
        self.get_each_row_mes_ou()  # ou 表

if __name__ == '__main__':
    a = SummaryData()
    a.run()