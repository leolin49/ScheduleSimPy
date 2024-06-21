# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/21 19:43
# Author  : linyf49@qq.com
# File    : csv_reader.py.py
import ast
import pandas as pd
from Infrastructure.edge_node import EdgeNode, EdgeNodeConfig
from Task.task import TaskConfig


def read_node_list_csv():
    node_list = []
    for chunk in pd.read_csv("Rd/node_list.csv", chunksize=1):
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
    task_data_list = []
    for chunk in pd.read_csv("Rd/task_list.csv", chunksize=1):
        for index, row in chunk.iterrows():
            # print(row)
            task = TaskConfig(
                int(row["id"]),
                float(row["submit_time"]),
                float(row["duration"]),
                float(row["transmit_time"]),
                int(row["cpu"]),
                float(row["memory"]),
                float(row["disk"]),
                str(row["ai_accelerator"]),
            )
            task_data_list.append(task)
    return task_data_list
