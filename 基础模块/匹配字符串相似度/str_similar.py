from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def simple_ratio(str1,str2):
    '''
    简单匹配相似度(常用)
    :param str1: 字符串1
    :param str2: 字符串2
    :return: 相似度
    '''
    similarity = fuzz.ratio(str1,str2)
    return similarity

def partial_ratio(str1,str2):
    '''
    非完全匹配，如一个字符串重开头开始到某处结束是另一字符串，则也算100
    str1 = 'hahahhjajj'
    str2 = 'hahahhja'  
    return:100
    :param str1: 字符串1
    :param str2: 字符串2
    :return: 相似度 
    '''
    similarity = fuzz.partial_ratio(str1, str2)
    return similarity

def token_sort_ratio(str1,str2):
    '''
    忽略顺序匹配
    :param str1: 字符串1
    :param str2: 字符串2
    :return: 相似度 
    '''
    similarity = fuzz.token_sort_ratio(str1, str2)
    return similarity

if __name__ == '__main__':
    str1 = 'a hahahhjjj'
    str2 = 'hahahhjjj a'
    s = token_sort_ratio(str1,str2)
    print(s)
