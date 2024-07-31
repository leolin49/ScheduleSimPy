# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:19
# Author  : linyf49@qq.com
# File    : scheduler.py.py
import time
from Task.task import Task
import util


# Base Scheduler class
class Scheduler(object):
    def __init__(self, name: str, env):
        self.name = name
        self.env = env
        self.simulator = None
        self.cluster = None
        self.scheduled_task_num = 0
        self.log = util.new_logger("./Log/" + name + ".Log", name)

    def attach(self, simulator):
        self.simulator = simulator
        self.cluster = simulator.cluster

    def run(self):
        while not self.simulator.finished:
            if len(self.cluster.unfinished_task_queue) > 0:
                task = self.cluster.unfinished_task_queue.popleft()
                self.schedule(task, self.env.now)
            yield self.env.timeout(1e-3)

    def schedule(self, task: Task, clock):
        s = time.time()
        node_id = self.make_decision(task, clock)
        if node_id == -1:
            self.log.warning(
                "now:{:.2f} task-{} schedule failed!!!".format(self.env.now, task)
            )
            return
        e = time.time()
        node = self.cluster.node_list[node_id - 1]
        task.schedule(node, (e - s) * 100)
        self.log.info(
            "now:{} task-{} is scheduled to Node-{}".format(
                self.env.now, task.id, node.id
            )
        )
        self.cluster.running_task_num += 1
        self.scheduled_task_num += 1
        if self.scheduled_task_num % 1000 == 0:
            print(
                f"now:{self.env.now} {self.scheduled_task_num} task is scheduled successfully."
            )

    def make_decision(self, task: Task, clock) -> int:
        pass
