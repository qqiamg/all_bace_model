import logging

def write_log():
# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  #级别由 debug<info<warning<error<critical

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('./test.log')

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()

# 定义handler的输出格式formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# 记录一条日志
logger.debug('logger debug message')
# logger.info('logger info message')
# logger.warning('logger warning message')
# logger.error('logger error message')
# logger.critical('logger critical message')
