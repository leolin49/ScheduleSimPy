# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:21
# Author  : linyf49@qq.com
# File    : cluster.py
from typing import List, Tuple
from Infrastructure.edge_node import EdgeNode


class Cluster:
    node_list: List[EdgeNode]

    def __init__(self):
        self.node_list = []

    # 添加边缘节点
    def add_node(self, node: EdgeNode, edges: List[Tuple] = None):
        self.node_list.append(node)

    # 获取集群中节点的数量
    def get_node_num(self):
        return len(self.node_list)
