# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/5/28 15:43
# Author  : linyf49@qq.com
# File    : data_product.py

import csv
from Rd import random as rd

node_list = rd.random_edge_node_list(100)

header = [
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
    writer.writerow(header)
    for node in node_list:
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
