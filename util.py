# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 20:35
# Author  : linyf49@qq.com
# File    : util.py.py

import numpy as np

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


def print_g(args, sep=" ", end="\n", file=None):
    print(Color.GREEN + args + Color.END)


def print_y(args, sep=" ", end="\n", file=None):
    print(Color.YELLOW + args + Color.END)


def print_r(args, sep=" ", end="\n", file=None):
    print(Color.RED + args + Color.END)


def is_dominates(x: np.ndarray, y: np.ndarray):
    return all(x >= y) and any(x > y)
