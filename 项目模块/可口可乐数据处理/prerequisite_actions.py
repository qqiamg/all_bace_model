from summary_data import SummaryData
from get_all_filterNo import GetFilter
from save_in_sqlite import SaveInSql
from transpose_table import TransposeTable

###执行所有前提操作###

SummaryData().run()  # 生成汇总表
GetFilter().run()  # 生成筛选项并设置表
SaveInSql().run()  # 把汇总表存入sqlite
TransposeTable().run()  # 生成转置表并保存
