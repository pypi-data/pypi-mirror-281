import logging

# 创建日志记录器
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# 创建处理器
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
print("logging")

def example_function():
    logger.debug("这是一个调试消息")
    logger.info("这是一个信息消息")
    logger.warning("这是一个警告消息")
    logger.error("这是一个错误消息")
    logger.critical("这是一个严重错误消息")

if __name__ == "__main__":
    example_function()
