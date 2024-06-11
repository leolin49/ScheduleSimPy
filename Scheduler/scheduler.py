# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:19
# Author  : linyf49@qq.com
# File    : scheduler.py.py
import time
from Infrastructure.cluster import Cluster
from Infrastructure.edge_node import EdgeNode
from Task.task import Task
import util


# 调度器基类
class Scheduler(object):
    def __init__(self, name: str, env):
        self.name = name
        self.env = env
        self.simulator = None
        self.cluster = None

    def attach(self, simulator):
        self.simulator = simulator
        self.cluster = simulator.cluster

    def run(self):
        while not self.simulator.finished:
            if len(self.cluster.unfinished_task_queue) > 0:
                task = self.cluster.unfinished_task_queue.popleft()
                self.schedule(task, self.env.now)
            yield self.env.timeout(0.1)

    def schedule(self, task: Task, clock):
        s = time.time()
        node_id = self.make_decision(task, clock)
        if node_id == -1:
            return
        node = self.cluster.node_list[node_id - 1]
        e = time.time()
        util.print_y(
            "now:{} task-{} is scheduled to Node-{} {}".format(
                self.env.now, task.id, node.id, node.__str__()
            )
        )
        task.schedule(node, e - s)

    def make_decision(self, task: Task, clock) -> int:
        pass
