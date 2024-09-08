# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 20:35
# Author  : linyf49@qq.com
# File    : util.py

import logging
import numpy as np

# -------------- Config ----------------
# k-means的K值
GROUP_COUNT = 3     
# 任务生成的时间范围
TIME_RANGE = 100    
# 任务数量的倍数
TASK_MUL = 5 
# 节点数量
NODE_NUM = 100
# --------------------------------------


GB = 1024


class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


MEMORY_CAPACITY = [
    512,
    1 * GB,
    # 2 * GB,
    4 * GB,
    8 * GB,
    16 * GB,
    32 * GB,
    # 64 * GB,
    # 128 * GB,
]
MEMORY_CAPACITY_SIZE = len(MEMORY_CAPACITY)

CPU_NUMBER = [1, 4, 12, 16, 32, 40]
CPU_NUMBER_SIZE = len(CPU_NUMBER)

# AI Accelerators Labels
AI_LABEL = [
    "GPU",

    "G2",
    "G3",
    "T4",
    "A10",
    "P100",
    "V100M16",
    "V100M32",

    "TPU",
    "NPU",
]

# Other Hardware Labels
LABEL = [
    "CPU",
    "RAM",
    "HDD",
    "SSD",
    "GBE",
]

ERROR_CODE_OK = 0
ERROR_CODE_INSUFFICIENT_CPU = 300
ERROR_CODE_INSUFFICIENT_MEM = 301
ERROR_CODE_INSUFFICIENT_GPU = 302


def print_g(args, sep=" ", end="\n", file=None):
    print(Color.GREEN + args + Color.END, sep, end, file)


def print_y(args, sep=" ", end="\n", file=None):
    print(Color.YELLOW + args + Color.END, sep, end, file)


def print_r(args, sep=" ", end="\n", file=None):
    print(Color.RED + args + Color.END, sep, end, file)


def is_dominates(x: np.ndarray, y: np.ndarray):
    return all(x >= y) and any(x > y)


def new_logger(log_file_path: str, name="Unknown Log name"):
    """
    Get logger
    :param log_file_path: Log file path
    :param name: Log name
    :return: logging object by default config
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    handler = logging.FileHandler(log_file_path)
    logger.addHandler(handler)
    return logger

