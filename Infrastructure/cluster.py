# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:21
# Author  : linyf49@qq.com
# File    : cluster.py
import math
from typing import List
from collections import deque
from Infrastructure.topology import Topology
from Infrastructure.edge_node import EdgeNode
import util


class Cluster:
    node_list: List[EdgeNode]

    def __init__(self):
        self.node_list = []
        self.unfinished_task_queue = deque()
        self.finished_task_list = []
        self.total_cpu = 0
        self.current_cpu = 0
        self.total_mem = 0
        self.current_mem = 0
        self.total_disk = 0
        self.current_disk = 0
        self.topology = Topology(self)
        self.running_task_num = 0
        self.total_task_num = 0

    def add_node(self, node: EdgeNode):
        node.attach(self)
        self.node_list.append(node)
        self.total_cpu += node.cpu_capacity
        self.current_cpu += node.cpu
        self.total_mem += node.mem_capacity
        self.current_mem += node.mem
        self.total_disk += node.disk_capacity
        self.current_disk += node.disk

    def add_edge(self, node_id1: int, node_id2: int, weight: int):
        self.topology.g[node_id1].append((node_id2, weight))

    def add_task(self, task):
        self.total_task_num += 1
        self.unfinished_task_queue.append(task)

    def insert_task(self, task):
        self.unfinished_task_queue.insert(0, task)

    @property
    def node_num(self) -> int:
        return len(self.node_list)

    def average_completion(self) -> float:
        total_time = 0
        task_num = len(self.finished_task_list)
        if task_num == 0:
            return 0
        for task in self.finished_task_list:
            total_time += task.finished_timestamp - task.started_timestamp
        return total_time / task_num

    @property
    def all_tasks_finished(self) -> bool:
        return len(self.unfinished_task_queue) == 0 and self.running_task_num == 0

    @property
    def cpu_capacity(self):
        return sum([node.cpu_capacity for node in self.node_list])

    @property
    def cpu(self):
        return sum([node.cpu for node in self.node_list])

    @property
    def cpu_utilization(self) -> float:
        return (self.cpu_capacity - self.cpu) / self.cpu_capacity * 100

    @property
    def mem_capacity(self):
        return sum([node.mem_capacity for node in self.node_list])

    @property
    def mem(self):
        return sum([node.mem for node in self.node_list])

    @property
    def mem_utilization(self) -> float:
        return (self.mem_capacity - self.mem) / self.mem_capacity * 100

    @property
    def gpu_capacity(self):
        return sum([node.gpu_capacity for node in self.node_list])

    @property
    def gpu(self):
        return sum([node.gpu for node in self.node_list])

    @property
    def gpu_utilization(self) -> float:
        return (self.gpu_capacity - self.gpu) / self.gpu_capacity * 100

    @property
    def state(self) -> str:
        return "cpu:{:.2f}% mem:{:.2f}% gpu:{:.2f}% todo_num:{} finish_num:{} total_num:{}".format(
            self.cpu_utilization,
            self.mem_utilization,
            self.gpu_utilization,
            len(self.unfinished_task_queue),
            len(self.finished_task_list),
            self.total_task_num,
        )

    def load_balance_state(self) -> List[float]:
        n = len(self.node_list)
        state = [[0] * (util.TIME_RANGE + 1) for _ in range(n + 1)]
        for task in self.finished_task_list:
            second = math.ceil(task.started_timestamp)
            if second == util.TIME_RANGE + 1:
                second -= 1
            node_id = task.work_node_id
            state[node_id][second] += 1
        res = [0] * (util.TIME_RANGE + 1)
        for second in range(1, util.TIME_RANGE + 1):
            total = 0
            for node_id in range(1, n + 1):
                total += state[node_id][second]
            avg = total / n
            total = 0
            for node_id in range(1, n + 1):
                total += (state[node_id][second] - avg) ** 2
            poor_mark = total / n
            res[second] = poor_mark
        return res
