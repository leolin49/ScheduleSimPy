# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/5/28 15:43
# Author  : linyf49@qq.com
# File    : data_product.py

import csv
import ast
import pandas as pd
from Infrastructure.edge_node import EdgeNode, EdgeNodeConfig
from Task.task import Task, TaskConfig
from Rd import random as rd

NEW_NODE_DATA = True
NEW_TASK_DATA = True

if NEW_NODE_DATA:
    # Node
    node_data = rd.random_edge_node_list(3000)
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
    task_list = rd.random_task_list(10)
    task_header = [
        "id",
        "submit_time",
        "duration",
        "instances_number",
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
                task.instances_number,
                task.cpu_consume,
                task.mem_consume,
                task.disk_consume,
                task.ai_accelerator,
                task.rely_data,
            ]
            writer.writerow(data)


def read_node_list_csv():
    node_list = []
    for chunk in pd.read_csv("node_list.csv", chunksize=1):
        for index, row in chunk.iterrows():
            # print(row)
            node = EdgeNode(
                row["id"],
                EdgeNodeConfig(
                    int(row["cpu_capacity"]),
                    int(row["mem_capacity"]),
                    int(row["disk_capacity"]),
                    int(row["bandwidth"]),
                    ast.literal_eval(row["labels"]),
                    int(row["cpu"]),
                    float(row["mem"]),
                    float(row["disk"]),
                ),
            )
            node_list.append(node)
    return node_list


def read_task_list_csv():
    task_list = []
    for chunk in pd.read_csv("task_list.csv", chunksize=1):
        for index, row in chunk.iterrows():
            # print(row)
            task = TaskConfig(
                int(row["id"]),
                float(row["submit_time"]),
                float(row["duration"]),
                int(row["instances_number"]),
                int(row["cpu"]),
                float(row["memory"]),
                float(row["disk"]),
                str(row["ai_accelerator"]),
            )
            task_list.append(task)
    return task_list
