# rs = 12
# a = pow(2,2)
# print(a)
import re
a = '一直一直爱你[憨笑] 啊啊啊啊明晚lala'
sub_comment = re.sub('\[.*?\]','',a)
print(sub_comment)