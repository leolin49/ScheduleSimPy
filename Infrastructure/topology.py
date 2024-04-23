# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/4 19:03
# Author  : linyf49@qq.com
# File    : topology.py

class Topology(object):
    def __init__(self, cluster):
        self.cluster = cluster
        self.node_num = cluster.node_num
        self.g = [[] for _ in range(self.node_num + 1)]
        for node in cluster.node_list:
            for neighbor_id, weight in node.edges:
                self.g[node.id].append((neighbor_id, weight))

