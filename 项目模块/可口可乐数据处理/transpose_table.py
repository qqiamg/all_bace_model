import pandas as pd
import os
import openpyxl
from copy import copy


###获取并生成转置表###

class TransposeTable(object):
    """
    生成转置表
    """

    def __init__(self):
        self.store_path = './table/by store/'
        self.save_path = './download_file/stroe_files/'
        self.title_file = './stc_title/bystore/'
        self.fitter_table = '2nd Display by Store'
        self.setting_list = {'SKU Availability by Store': ['24C', 'Abs'], 'SKU Facing by Store': ['32C', 'Abs'],
                             'SKU Price by Store': ['71C', 'Abs'], 'SOVI by Store': ['31C', 'Abs'],
                             'Cooler by Store': ['44C', '41C', '42C', '43C', 'Abs'],
                             '2nd Display by Store': ['51C', '54C', 'Abs'],
                             'Thematic by Store': ['61C', '%']}
        if not os.path.exists(self.save_path):  # 新建文件夹
            os.makedirs(self.save_path)

    def read_transpose(self):
        """
        读取转置表的数据
        :return:
        """
        if self.fitter_table == 'SKU Availability by Store':
            df = pd.read_excel(self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                               sheet_name='{}'.format(self.setting_list[self.fitter_table][0]), header=8,
                               index_col=0)  # 以第8行作为标题
            df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
            com_df = df2.iloc[0:, 4:].fillna(0)  # 除nan 为0
            all_title_name = list(com_df.columns.values)  # 获取所有表头
            # print(all_title_name)
            for i in all_title_name[:-3]:
                com_df[i] = com_df[i].apply(lambda x: format(x, '.0%'))
                com_df[i] = com_df[i].replace(['0%'], [''])
            for i in all_title_name[-3:]:
                com_df[i] = com_df[i].apply(lambda x: str(x) + "%")
        elif self.fitter_table == 'SKU Facing by Store':
            df = pd.read_excel(self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                               sheet_name='{}'.format(self.setting_list[self.fitter_table][0]), header=8,
                               index_col=0)  # 以第8行作为标题
            df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
            com_df = df2.iloc[0:, 3:].fillna(0)  # 除nan 为0
            all_title_name = list(com_df.columns.values)  # 获取所有表头
            # print(all_title_name)
            for one_title in all_title_name:
                if 'vs' in one_title:
                    com_df[one_title] = com_df[one_title].apply(lambda x: format(x, '.0%'))  # 转百分比
        elif self.fitter_table == 'SKU Price by Store':
            df = pd.read_excel(self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                               sheet_name='{}'.format(self.setting_list[self.fitter_table][0]), header=8,
                               index_col=0)  # 以第8行作为标题
            df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
            com_df = df2.iloc[0:, 3:].fillna(0)  # 除nan 为0
        elif self.fitter_table == 'SOVI by Store':
            df = pd.read_excel(self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                               sheet_name='{}'.format(self.setting_list[self.fitter_table][0]), header=8,
                               index_col=0)  # 以第8行作为标题
            df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
            com_df = df2.iloc[0:, 3:].fillna(0)  # 除nan 为0
            all_title_name = list(com_df.columns.values)  # 获取所有表头
            for i in all_title_name:
                com_df[i] = com_df[i].apply(lambda x: format(x, '.0%'))
                com_df[i] = com_df[i].replace(['0%'], [''])
            lins_list = [x for x in all_title_name if 'NET' in x]
            com_df = com_df.drop(lins_list, axis=1)  # 清除不需要的列
            # print(com_df)
        elif self.fitter_table == 'Cooler by Store':  # 有两个表组成的，要拿多一个
            ##第一个表## (44C) 百分比
            df = pd.read_excel(self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                               sheet_name='{}'.format(self.setting_list[self.fitter_table][0]), header=8,
                               index_col=0)  # 以第8行作为标题
            df1 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
            com_df = df1.iloc[0:, 3:].fillna(0)  # 除nan 为0
            all_title_name = list(com_df.columns.values)  # 获取所有表头
            for i in all_title_name:
                com_df[i] = com_df[i].apply(lambda x: format(x, '.0%'))
                com_df[i] = com_df[i].replace(['0%'], [''])
            if len(self.setting_list[self.fitter_table]) >= 3:  # 判断是不是有第二个表
                for one_table in self.setting_list[self.fitter_table][1:-1]:
                    if one_table == '41C' or one_table == '42C':
                        ##第二、三个表##（41C 、42C直接显示)
                        df2 = pd.read_excel(
                            self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                            sheet_name='{}'.format(one_table), header=8,
                            index_col=0)  # 以第8行作为标题
                        df3 = pd.DataFrame(df2.values.T, index=df2.columns, columns=df2.index)
                        com_df_next = df3.iloc[0:, 3:].fillna(0)  # 除nan 为0
                        # com_df = com_df.join(com_df_next)
                        com_df = pd.merge(com_df, com_df_next, left_index=True, right_index=True)
                    if one_table == '43C':
                        ##第四个表##（43C 显示百分比)
                        df2 = pd.read_excel(
                            self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                            sheet_name='{}'.format(one_table), header=8,
                            index_col=0)  # 以第8行作为标题
                        df3 = pd.DataFrame(df2.values.T, index=df2.columns, columns=df2.index)
                        com_df_next = df3.iloc[0:, 3:].fillna(0)  # 除nan 为0
                        all_title_name = list(com_df_next.columns.values)  # 获取所有表头
                        for i in all_title_name:
                            com_df_next[i] = com_df_next[i].apply(lambda x: format(x, '.0%'))
                            com_df_next[i] = com_df_next[i].replace(['0%'], [''])
                        # com_df = com_df.join(com_df_next)
                        com_df = pd.merge(com_df, com_df_next, left_index=True, right_index=True)
        elif self.fitter_table == 'Thematic by Store':
            df = pd.read_excel(self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                               sheet_name='{}'.format(self.setting_list[self.fitter_table][0]), header=8,
                               index_col=0)  # 以第8行作为标题
            df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
            com_df = df2.iloc[0:, 4:].fillna(0)  # 除nan 为0
            all_title_name = list(com_df.columns.values)  # 获取所有表头
            for i in all_title_name:
                com_df[i] = com_df[i].apply(lambda x: format(x, '.0%'))
        else:  # 其他为 2nd Display by Store
            ##第一个表 51C (转百分比)
            df = pd.read_excel(self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                               sheet_name='{}'.format(self.setting_list[self.fitter_table][0]), header=8,
                               index_col=0)  # 以第8行作为标题
            df2 = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
            com_df = df2.iloc[0:, 3:].fillna(0)  # 除nan 为0
            all_title_name = list(com_df.columns.values)  # 获取所有表头
            for i in all_title_name:
                com_df[i] = com_df[i].apply(lambda x: format(x, '.0%'))
                com_df[i] = com_df[i].replace(['0%'], [''])
            if len(self.setting_list[self.fitter_table]) >= 3:  # 判断是不是有第二个表
                for one_table in self.setting_list[self.fitter_table][1:-1]:
                    if one_table == '54C':
                        ##第二个表##（54C 部分百分比)
                        df2 = pd.read_excel(
                            self.store_path + 'table({}).xlsx'.format(self.setting_list[self.fitter_table][-1]),
                            sheet_name='{}'.format(one_table), header=8,
                            index_col=0)  # 以第8行作为标题
                        df3 = pd.DataFrame(df2.values.T, index=df2.columns, columns=df2.index)
                        all_title_name = list(df3.columns.values)  # 获取所有表头
                        lins_list = [x for x in all_title_name if 'NET' in str(x)]
                        com_df_next = df3.iloc[0:, 3:].fillna(0)  # 除nan 为0
                        com_df_next = com_df_next.drop(lins_list, axis=1)  # 清除不需要的列
                        all_title_name = list(com_df_next.columns.values)  # 获取所有表头
                        for i in all_title_name:
                            if '%' in str(i):
                                com_df_next[i] = com_df_next[i].apply(lambda x: format(x, '.0%'))
                        com_df = pd.merge(com_df, com_df_next, left_index=True, right_index=True)
        store_df = pd.read_excel('测试设置表.xlsx', sheet_name='pop')  # 查询拼接店铺信息
        store_df = store_df.loc[:, ['BG', 'OU', 'City', 'Channel', 'Banner', 'POP_id', 'POP']]
        zz_df = pd.merge(com_df, store_df, left_index=True, right_on="POP")
        one_df = zz_df.iloc[:, -7:]
        two_df = zz_df.iloc[:, :-7]
        new_df = one_df.join(two_df)  # 完整数据
        self.get_com_table(new_df)

    def get_com_table(self, table_data):
        """生成完整表(索引拿完了，差填数据)"""
        zimu = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
        max_lie = table_data.shape[1]  # 最大列数
        # 生成完整表
        title_wb = openpyxl.load_workbook(self.title_file + '{}.xlsx'.format(self.fitter_table))  # 读取标题表
        title_ws = title_wb.active
        all_data = []
        for one_row in table_data.iterrows():  # 获取数据
            all_data.append(list(one_row[1]))
        # 生成索引
        if max_lie <= 26:  # 处理标题的长度对应的字母
            mes_zm = zimu[:max_lie]
        else:
            else_zm_len = max_lie - 26
            mes_zm = copy(zimu)
            num = 0
            for f_zm in zimu:
                if num >= else_zm_len:
                    break
                for s_zm in zimu:
                    if num >= else_zm_len:
                        break
                    ex_zm = f_zm + s_zm
                    mes_zm.append(ex_zm)
                    num += 1
        # 填数据
        for z, one_data in enumerate(all_data):
            for j, data in enumerate(one_data):
                if self.fitter_table == 'SOVI by Store':
                    title_ws['{}{}'.format(mes_zm[j], z + 5)] = data
                else:
                    title_ws['{}{}'.format(mes_zm[j], z + 4)] = data
        title_wb.save(self.save_path + '{}.xlsx'.format(self.fitter_table))

    def run(self):
        for one_table in self.setting_list:
            print(one_table)
            self.fitter_table = one_table
            self.read_transpose()


if __name__ == '__main__':
    a = TransposeTable()
    a.run()
