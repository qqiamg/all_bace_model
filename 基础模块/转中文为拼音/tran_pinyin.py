from pypinyin import pinyin, lazy_pinyin

def pinyin_name(c_name):
    '''
    翻译中文名为拼音构成的英文名
    :param c_name: 中文名
    :return: 英文名
    '''
    try:
        name = lazy_pinyin(c_name)
        name_list = []
        c_name = ''
        if len(name) == 1:
            pinyin_name = a
            pass
        else:
            for one in name:
                if name_list == []:
                    name_list.append(one)
                else:
                    c_name += one
            name_list.append(c_name)
            L2 = list(map(lambda a: a.capitalize(), name_list)) #capitalize() 首字母大写
            pinyin_name = ' '.join(L2)
        return pinyin_name
    except:
        print('出错,返回中文名')
        return c_name

def t_pinyin(mes):
    '''
    翻译中文为拼音
    :param mes: 需要翻译的内容
    :return: 一个列表，包含每个字的拼音
    '''
    name = lazy_pinyin(mes)
    return name

if __name__ == '__main__':
    a = pinyin_name('黄兴华')
    print(a)