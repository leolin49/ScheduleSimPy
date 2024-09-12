# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/17 20:21
# Author  : linyf49@qq.com
# File    : lrr.py
"""
It is a scoring function provided by Kubernetes,
which determines the score by the ratio of idle resources to the total amount of resources.
It tries to schedule Pods to nodes that consume relatively small computing resources.
The more idle resources, the higher the score. CPU and memory share the same weight.
It is the most widely used scoring function.

Score = [(C_cpu-U_cpu)/C_cpu*10 + (C_mem-U_mem)/C_mem*10] / 2
"""
from Scheduler.scheduler import Scheduler
from Task.task import Task


class LeastRequestedPriority(Scheduler):
    def __init__(self, name: str, env):
        super(LeastRequestedPriority, self).__init__(name, env)

    def make_decision(self, task: Task, clock) -> int:
        scores = [0] * self.cluster.node_num
        ids = [i for i in range(self.cluster.node_num)]
        for i, node in enumerate(self.cluster.node_list):
            scores[i] = (
                ((node.cpu / node.cpu_capacity) * 10)
                + ((node.mem / node.mem_capacity) * 10)
            ) / 2
        ids.sort(key=lambda i: -scores[i])
        for idx in ids[:]:
            ok, err = self.cluster.node_list[idx].can_run_task(task)
            if ok:
                return idx + 1
        return -1
