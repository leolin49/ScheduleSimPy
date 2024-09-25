# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/17 20:34
# Author  : linyf49@qq.com
# File    : bra.py
"""
BalancedResourceAllocation is a scoring function provided by Kubernetes,
which is to calculate the difference between CPU utilization and memory utilization.
The smaller the difference, the more balanced the CPU and memory utilization, and the higher the score.
This approach tries to choose nodes with more balanced resources after Pod is deployed.
However, this function cannot be used alone, and it must be used together with LeastRequestedPriority,
because if the requested resource (CPU or memory) is greater than the total capacity of the node,
the node will never be scheduled.

Score = [1 - abs(R_cpu / C_cpu - R_mem / C_mem)] * 10
"""


from Scheduler.scheduler import Scheduler
from Task.task import Task

import util


class BalancedResourceAllocation(Scheduler):
    def __init__(self, name: str, env):
        super(BalancedResourceAllocation, self).__init__(name, env)

    def make_decision(self, task: Task, clock) -> int:
        scores = [0] * self.cluster.node_num
        ids = [i for i in range(self.cluster.node_num)]
        for i, node in enumerate(self.cluster.node_list):
            a = (node.cpu_capacity - node.cpu + task.cpu_consume) / node.cpu_capacity
            b = (node.mem_capacity - node.mem + task.mem_consume) / node.mem_capacity
            scores[i] = (1 - abs(a - b)) * 10
        ids.sort(key=lambda i: -scores[i])
        for idx in ids:
            ok, err = self.cluster.node_list[idx].can_run_task(task)
            if ok:
                return idx + 1
        return -1
