# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 20:31
# Author  : linyf49@qq.com
# File    : random_infrastructure.py.py
import random
from typing import List
import random as rd

from Infrastructure.edge_node import EdgeNode, EdgeNodeConfig
import util


def random_edge_node(node_id: int, level: int) -> EdgeNode:
    memory = rd.choice(util.MEMORY_CAPACITY[level * 3 - 3 : level * 3])
    node = EdgeNode(node_id, EdgeNodeConfig(64, memory, memory * 10, 100))

    node.cpu = 64 * random.random()
    node.mem = memory * random.random()
    node.disk = 10 * memory * random.random()
    node.container_num = random.randint(1, 20)

    return node


def random_edge_node_list(n: int) -> List[EdgeNode]:
    node_list = []
    for i in range(n):
        node = None
        if i < int(n * 0.6):
            node = random_edge_node(i, 1)
        elif i < int(n * 0.9):
            node = random_edge_node(i, 2)
        else:
            node = random_edge_node(i, 3)
        node_list.append(node)
    return node_list
