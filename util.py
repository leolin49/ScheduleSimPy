# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 20:35
# Author  : linyf49@qq.com
# File    : util.py.py
import time

GB = 1024

MEMORY_CAPACITY = [
    512,
    1 * GB,
    2 * GB,
    4 * GB,
    8 * GB,
    16 * GB,
    32 * GB,
    64 * GB,
    128 * GB,
]


def run_with_time(func):
    start_time = time.time()
    node = func()
    print("node_info: ", node.__str__())
    end_time = time.time()
    print("execution_time：", (end_time - start_time) * 1000, " ms")
