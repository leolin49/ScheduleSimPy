# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 20:31
# Author  : linyf49@qq.com
# File    : random.py.py

import random
from typing import List

from Infrastructure.edge_node import EdgeNode, EdgeNodeConfig
from Task.task import Task, TaskConfig
import util


def random_edge_node(node_id: int, level: int) -> EdgeNode:
    cpu = random.choice(util.CPU_NUMBER[(level - 1) * util.CPU_NUMBER_SIZE // 3: level * util.CPU_NUMBER_SIZE // 3])
    memory = random.choice(util.MEMORY_CAPACITY[(level - 1) * util.MEMORY_CAPACITY_SIZE // 3: level * util.MEMORY_CAPACITY_SIZE // 3])
    node = EdgeNode(node_id, EdgeNodeConfig(cpu, memory, memory * 10, 100))
    node.labels = random.sample(util.LABEL, 2)
    if level >= 2:  # level大于2的才有AI加速器
        node.labels.append(random.choice(util.AI_LABEL))
    node.cpu = cpu * random.random()
    node.mem = memory * random.random()
    node.disk = 10 * memory * random.random()
    node.container_num = random.randint(1, 20)

    return node


def random_edge_node_list(n: int) -> List[EdgeNode]:
    node_list = []
    for i in range(1, n + 1):
        node = None
        if i < int(n * 0.6):
            node = random_edge_node(i, 1)
        elif i < int(n * 0.9):
            node = random_edge_node(i, 2)
        else:
            node = random_edge_node(i, 3)
        node_list.append(node)
    return node_list


def random_task(env, task_id: int, task_type: int = 1) -> TaskConfig:
    submit_time = random.uniform(1, 10)
    duration = random.uniform(0.0001, 1.1432) * random.uniform(1, 1.7520 / 0.4883)
    mem = random.randint(50, 250)
    cpu = random.randint(1, 4)
    disk = random.randint(100, 500)
    ai_accelerator = random.choice(util.AI_LABEL)
    return TaskConfig(task_id, submit_time, duration, 1, cpu, mem, disk, ai_accelerator)


def random_task_list(env, n: int) -> List[TaskConfig]:
    task_configs = []
    for i in range(1, n + 1):
        task_config = random_task(env, i)
        task_configs.append(task_config)
    task_configs.sort(key=lambda t: t.submit_time)
    return task_configs


def test_task(env) -> List[TaskConfig]:
    task_configs = [
        TaskConfig(1, 10, 3, 1, 2, 100, 100, "GPU", None),
        TaskConfig(2, 10.5, 0.8421, 1, 2, 100, 100, "TPU", None),
        TaskConfig(3, 10.5, 0.1168, 1, 2, 100, 100, "NPU", None),
    ]
    return task_configs