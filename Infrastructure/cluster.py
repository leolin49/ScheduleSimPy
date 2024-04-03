# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:21
# Author  : linyf49@qq.com
# File    : cluster.py
from typing import List, Tuple
from collections import deque
from math import inf
from Infrastructure.edge_node import EdgeNode, EdgeNodeConfig
from Infrastructure.cloud_node import CloudNode

INF = 10 ** 18


class Cluster:
    node_list: List[EdgeNode]

    def __init__(self):
        self.node_list = [CloudNode(0, EdgeNodeConfig(INF, INF, INF, INF))]
        self.unfinished_task_queue = deque()
        self.finished_task_list = []

    # 添加边缘节点
    def add_node(self, node: EdgeNode, edges: List[Tuple] = None):
        self.node_list.append(node)

    def add_task(self, task):
        self.unfinished_task_queue.append(task)

    # 获取集群中节点的数量
    def node_num(self):
        return len(self.node_list)

    @property
    def all_tasks_finished(self) -> bool:
        return len(self.unfinished_task_queue) == 0

