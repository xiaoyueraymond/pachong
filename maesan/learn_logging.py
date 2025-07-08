import logging
import os
import sys

# 获取当前 Python 脚本文件的路径
current_script_path = os.path.abspath(sys.argv[0])
current_script_directory = os.path.dirname(current_script_path)
print(f"当前脚本文件路径: {current_script_path}")
print(f"当前脚本文件所在目录: {current_script_directory}")

# 指定日志文件的相对路径
log_file_path = os.path.join(current_script_directory, 'temp.log')

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志记录器的级别为 DEBUG

# 创建文件处理器，指定日志文件路径和编码
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.WARNING)  # 设置文件处理器的级别为 WARNING
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# 创建流处理器，将日志输出到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  # 设置流处理器的级别为 DEBUG
stream_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)

# 添加处理器到日志记录器
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# 记录不同级别的日志信息
logger.debug('调试信息')
logger.info('消息日志')
logger.warning('警告日志')
logger.error('错误日志')
logger.critical('严重错误')
