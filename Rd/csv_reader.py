# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/21 19:43
# Author  : linyf49@qq.com
# File    : csv_reader.py
import ast
import random
import pandas as pd

import util
from Infrastructure.edge_node import EdgeNode, EdgeNodeConfig
from Task.task import TaskConfig

ALIBABA_TASK_LIST = []
ALIBABA_NODE_LIST = []


def read_node_list_csv():
    node_list = []
    for chunk in pd.read_csv("Rd/node_list.csv", chunksize=1):
        for index, row in chunk.iterrows():
            # print(row)
            lbs = ast.literal_eval(row["labels"])
            cnt = [1] * len(lbs)
            node = EdgeNode(
                row["id"],
                EdgeNodeConfig(
                    int(row["cpu_capacity"]),
                    int(row["mem_capacity"]),
                    int(row["disk_capacity"]),
                    1,
                    int(row["bandwidth"]),
                    lbs,
                    cnt,
                    cpu=int(row["cpu"]),
                    memory=float(row["mem"]),
                    disk=float(row["disk"]),
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
                str(row["ai_accelerator"]).split("|"),
                1,
            )
            task_list.append(task)
    return task_list


def read_alibaba_task_list_csv(file: str):
    for chunk in pd.read_csv(file, chunksize=1):
        for index, row in chunk.iterrows():
            task_id = int(row["name"][-4:]) + 1
            ais = None
            gpu_spec_str = str(row["gpu_spec"])
            if gpu_spec_str != "nan":
                ais = gpu_spec_str.split("|")
            # if ais is None:
            #     continue
            if str(row["scheduled_time"]) == "nan":
                continue
            task = TaskConfig(
                task_index=task_id,
                # submit_time=random.uniform(1, util.TIME_RANGE),
                submit_time=util.rand_float(1, util.TIME_RANGE),
                duration=random.uniform(0.0001, 1.1432)
                * random.uniform(1, 1.7520 / 0.4883),
                # submit_time=int(row["creation_time"]),
                # duration=int(row["deletion_time"]) - int(row["scheduled_time"]),
                transmit_time=random.uniform(0.2985, 1.5926),
                cpu=int(row["cpu_milli"]) // 1000,
                memory=int(row["memory_mib"]),
                disk=0,
                ai_accelerators=ais,
                ai_accelerator_num=int(row["num_gpu"]),
            )
            ALIBABA_TASK_LIST.append(task)


def read_alibaba_node_list_csv(file: str):
    initial_state = {"gpu": 1, "cpu": 0.75, "mem": 0.75}  # 控制初始的资源数量
    for chunk in pd.read_csv(file, chunksize=1):
        for index, row in chunk.iterrows():
            node_id = int(row["sn"][-4:]) + 1
            cpu_capacity = int(row["cpu_milli"]) // 1000
            mem_capacity = int(row["memory_mib"])
            lbs = None
            cnt = None
            if str(row["model"]) != "nan":
                lbs = row["model"].split(",")
                cnt = [int(c) for c in str(row["gpu"]).split(",")]
            node = EdgeNode(
                node_id,
                EdgeNodeConfig(
                    cpu_capacity,
                    mem_capacity,
                    1048576,  # 1TB
                    int(row["gpu"]),
                    100,
                    lbs,
                    cnt,
                    cpu_capacity * initial_state["cpu"],
                    mem_capacity * initial_state["mem"],
                    1048576 // 2,
                    # initial_gpu
                ),
            )
            ALIBABA_NODE_LIST.append(node)
