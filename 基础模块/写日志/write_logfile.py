import logging
import os

def write_log(file_path,log_txt,d_type=False):
    """
    写日志
    :param file_path: 日志的路径 如：'./sys_files/logs.log'
    :param log_txt: 记录的文本
    :param d_type: 记录的类型 True 为 debug ，False 为 error
    :return:
    """
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  #级别由 debug < info < warning < error < critical

    # 创建一个handler，用于写入日志文件
    z = file_path.count("/")
    if z <=1:
        pass
    else:
        file_d = file_path.replace(f"{file_path.split('/')[-1]}",'')
        if not os.path.exists(file_d):  # 新建文件夹
            os.makedirs(file_d)
    fh = logging.FileHandler(file_path)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()

    # 定义handler的输出格式formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    # 记录一条日志
    if d_type: #是否是记录错误
        logger.error(log_txt)
    else:
        logger.debug(log_txt)

if __name__ == '__main__':
    write_log('./sys/text.txt','success',d_type=True)

    # file_path = './sys/text.txt'
    # file_path = file_path.replace(file_path.split('/')[-1],'')
    # print(file_path)