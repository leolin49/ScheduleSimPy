# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/21 19:43
# Author  : linyf49@qq.com
# File    : csv_reader.py.py
import ast
import random
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
    task_list = []
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
                1,
            )
            task_list.append(task)
    return task_list


def read_alibaba_task_list_csv():
    task_list = []
    for chunk in pd.read_csv('Dataset/cluster-trace-gpu-v2023/csv/openb_pod_list_gpuspec33.csv', chunksize=1):
        for index, row in chunk.iterrows():
            task_id = int(row['name'][-4:]) + 1
            task = TaskConfig(
                task_index=task_id,
                submit_time=random.uniform(1, 100),
                duration=random.uniform(0.0001, 1.1432) * random.uniform(1, 1.7520 / 0.4883),
                transmit_time=random.uniform(0.2985, 1.5926),
                cpu=int(row['cpu_milli']) // 1000,
                memory=int(row['memory_mib']) // 1024,
                disk=0,
                ai_accelerator=str(row['gpu_spec']),
                ai_accelerator_num=int(row['num_gpu']),
            )
            task_list.append(task)
    return task_list


def read_alibaba_node_list_csv():
    node_list = []
    for chunk in pd.read_csv("Dataset/cluster-trace-gpu-v2023/csv/openb_node_list_all_node.csv", chunksize=1):
        for index, row in chunk.iterrows():
            node_id = int(row['sn'][-4:]) + 1
            cpu_capacity = int(row['cpu_milli']) // 1000
            mem_capacity = int(row['memory_mib']) // 1024
            node = EdgeNode(
                node_id,
                EdgeNodeConfig(
                    cpu_capacity,
                    mem_capacity,
                    1048576,    # 1TB
                    100,
                ),
            )
            node_list.append(node)
    return node_list
