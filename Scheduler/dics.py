# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:28
# Author  : linyf49@qq.com
# File    : dics.py
from math import sqrt

from Scheduler.scheduler import Scheduler
from Task.task import Task


class DataIntensiveContainerScheduling(Scheduler):
    def __init__(self, name: str, env):
        super(DataIntensiveContainerScheduling, self).__init__(name, env)
        self.F1 = [1, 1, 1, -1, 1]
        self.W = [0.2, 0.2, 0.2, 0.2, 0.2]
        self.criteria_num = len(self.F1)

    @staticmethod
    def can_run(task: Task, node) -> bool:
        return (
            task.cpu_consume <= node.cpu_capacity
            and task.mem_consume <= node.mem_capacity
        )

    def make_decision(self, task: Task, clock) -> int:
        # prepare
        esp = 1e-6
        ids = []
        info = []
        for node in self.cluster.node_list:
            if not self.can_run(task, node):
                continue
            ids.append(node.id)
            info.append(
                [
                    node.cpu_utilization,
                    node.mem_utilization,
                    node.disk_utilization,
                    node.container_num,
                    node.bandwidth,
                ]
            )

        k = len(info)
        c = self.criteria_num
        """
        Step 1.
        Construct decision matrix self._inf (input), which is filled with 
        1. CPU utilization rate, 
        2. memory utilization rate, 
        3. disk I/O speed, 
        4. the number of containers currently running on node, 
        5. network transmission bandwidth. 
        For example, if the CPU utilization rate is 50%, the element is filled with 50 directly.
        """
        """
        Step 2.
        Construct the normalized decision matrix E.
        """
        tmp = [sqrt(sum(info[i][j] ** 2 for i in range(k))) for j in range(c)]
        E = [
            [(info[i][j] / (tmp[j] + esp) if tmp[j] else 0) for j in range(c)]
            for i in range(k)
        ]
        """
        Step 3.
        Construct the weighted normalized decision matrix S, using the weighting factors W
        """
        S = [[self.W[j] * E[i][j] for j in range(c)] for i in range(k)]
        """
        Step 4.
        According to our goal, determine the ideal and negative ideal solutions (A+ and A−, respectively) 
        for each indicator from each column in the matrix S
        """
        A1 = [
            (
                max(S[i][j] for i in range(k))
                if self.F1[j] == 1
                else min(S[i][j] for i in range(k))
            )
            for j in range(c)
        ]
        A2 = [
            (
                min(S[i][j] for i in range(k))
                if self.F1[j] == 1
                else max(S[i][j] for i in range(k))
            )
            for j in range(c)
        ]
        """
        Step 5.
        Calculate the separation measures for each alternative.
        """
        B1 = [0.0] * k
        B2 = [0.0] * k
        for i in range(k):
            B1[i] = sqrt(sum((A1[j] - S[i][j]) ** 2 for j in range(c)))
            B2[i] = sqrt(sum((S[i][j] - A2[j]) ** 2 for j in range(c)))
        """
        Step 6.
        Calculate the relative closeness to the ideal solution, which is denoted as RCi.
        """
        RC = [B2[i] / (B1[i] + B2[i] + esp) for i in range(k)]
        """
        All alternative nodes are ranked according to the value of RC.
        The node with the highest value of RC is the target node to execute container. 
        If there are more than one node with the same RC, we randomly choose one.
        """
        combined = list(zip(ids, RC))
        sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
        sorted_ids = [id for id, _ in sorted_combined]
        for nid in sorted_ids:
            ok, err = self.cluster.node_list[nid - 1].can_run_task(task)
            if ok:
                return nid
        return -1
