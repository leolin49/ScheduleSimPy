# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 20:35
# Author  : linyf49@qq.com
# File    : util.py

import logging
import cProfile
import pstats
import secrets

from guppy import hpy

import numpy as np


# -------------- Config ----------------

BASELINE_NAME = ["bra", "dics", "kcss", "lrp", "odcs", "rccs"]

# k-means的K值
GROUP_COUNT = 3

# 执行延迟系数
DELAY_FACTOR = 3.6

# 任务生成的时间范围
TIME_RANGE = 100

# 任务样本数量
TASK_NUM = 4000

DECISION_MUL = 100

# 节点采样是否随机
RANDOM_NODE_SAMPLE = False

# 节点样本数 & 任务数量的倍数
# NODE_NUM, TASK_MUL = 50, [2, 3, 4, 5, 6]
NODE_NUM, TASK_MUL = 100, [4, 5, 6, 7, 8]
# NODE_NUM, TASK_MUL = 200, [9, 11, 13, 15, 17]
# NODE_NUM, TASK_MUL = 300, [11, 15, 19, 23, 27]

# 仅用于测量调度时间
NODE_MUL = 1
TIME_TEST_ON = False
# NODE_NUM, TASK_MUL = 1000, [4, 5, 6, 7, 8]

# Baseline 图例颜色
# BASELINE_COLORS = ['#1f78b4', '#e31a1c', '#ff7f00', '#6a3d9a', '#b15928', '#33a02c']
# BASELINE_COLORS= ["brown", "green", "purple", "orange", "blue", "red"]

# RGB
COLORS = [
    # ------
    ("038", "070", "083"),
    # ("042", "157", "142"),
    ("138", "176", "125"),
    ("233", "196", "107"),
    ("243", "162", "097"),
    ("230", "111", "081"),
    ("042", "157", "142"),
    # ------
    # ("246", "111", "105"),
    # ------
    ("248", "230", "032"),
    ("065", "062", "013"),
    ("048", "104", "141"),
    ("031", "146", "139"),
    ("053", "183", "119"),
    ("068", "004", "090"),
    ("145", "213", "066"),
    # ------
]

BASELINE_COLORS = [
    (int(c[0]) / 255, int(c[1]) / 255, int(c[2]) / 255)
    for c in [(x, y, z) for x, y, z in COLORS]
]

# CDF采集时间间隔 (ms)
CDF_INTERVAL = 100
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


ENABLE_MEMORY_PROFILE = False
baseline_tested = {baseline_name: 0 for baseline_name in BASELINE_NAME}


def memory_profile(func):
    executed = 0

    def wrapper(*args, **kwargs):
        nonlocal executed
        if executed < 3:
            h = hpy()
            before = h.heap()
            res = func(*args, **kwargs)
            after = h.heap()
            diff = after - before
            print(
                "{}-{} Memory diff: {}KB".format(
                    func.__module__, func.__name__, diff.size
                )
            )
            executed += 1
            return res
        return func(*args, **kwargs)

    return wrapper


def toggle_memory_profile(func):
    # baseline_name = func.__module__.split('.')[1]
    if not ENABLE_MEMORY_PROFILE:
        return func
    # baseline_tested[baseline_name] = True
    return memory_profile(func)


def rand_float(low: int, high: int):
    rd = secrets.randbelow(100_000) / 100_000
    return low + (high - low) * rd


def rand_int(low: int, high: int):
    return secrets.randbelow(high - low + 1) + low
