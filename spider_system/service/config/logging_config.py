# logging_config.py
import logging
from colorama import Fore, Style, init
import sys

# 初始化 Colorama
init(autoreset=True)

# 创建自定义日志格式化器
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.DEBUG:
            record.msg = f"{Fore.BLUE}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.INFO:
            record.msg = f"{Fore.GREEN}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.WARNING:
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        elif record.levelno == logging.CRITICAL:
            record.msg = f"{Fore.RED}{Style.BRIGHT}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:     %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
    logger = logging.getLogger("uvicorn.error")
    for handler in logger.handlers:
        handler.setFormatter(ColoredFormatter('%(levelname)s:     %(message)s'))

    logger = logging.getLogger("uvicorn.access")
    for handler in logger.handlers:
        handler.setFormatter(ColoredFormatter('%(levelname)s:     %(message)s'))