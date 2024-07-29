# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/5/28 15:43
# Author  : linyf49@qq.com
# File    : data_product.py

import csv
from Rd import data_random as rd

NEW_NODE_DATA = True
NEW_TASK_DATA = True

if NEW_NODE_DATA:
    # Node
    node_data = rd.random_edge_node_list(100)
    node_header = [
        "id",
        "cpu_capacity",
        "cpu",
        "mem_capacity",
        "mem",
        "disk_capacity",
        "disk",
        "bandwidth",
        "running_task",
        "labels",
    ]
    with open("node_list.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(node_header)
        for node in node_data:
            data = [
                node.id,
                node.cpu_capacity,
                node.cpu,
                node.mem_capacity,
                node.mem,
                node.disk_capacity,
                node.disk,
                node.bandwidth,
                node.container_num,
                node.labels,
            ]
            writer.writerow(data)

if NEW_TASK_DATA:
    # Task
    task_list = rd.random_task_list(10000)
    task_header = [
        "id",
        "submit_time",
        "duration",
        "transmit_time",
        "cpu",
        "memory",
        "disk",
        "ai_accelerator",
        "rely_data",
    ]
    with open("task_list.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(task_header)
        for task in task_list:
            data = [
                task.id,
                task.submit_time,
                task.duration,
                task.transmit_time,
                task.cpu_consume,
                task.mem_consume,
                task.disk_consume,
                task.ai_accelerators,
                task.rely_data,
            ]
            writer.writerow(data)



