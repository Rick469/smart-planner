import logging
import os

# 日志目录
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 创建 logger
log = logging.getLogger("smart-planner")
log.setLevel(logging.INFO)

# 避免重复添加 handler
if not log.handlers:

    # 文件输出
    file_handler = logging.FileHandler(
        f"{LOG_DIR}/smart-planner.log",
        encoding="utf-8"
    )

    # 控制台输出
    console_handler = logging.StreamHandler()

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)