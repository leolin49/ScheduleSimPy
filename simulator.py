# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/1 17:01
# Author  : linyf49@qq.com
# File    : simulator.py.py
from simpy import Environment

import util


class Simulator(object):
    def __init__(self, env: Environment, cluster, scheduler, task_broker, monitor):
        self.env = env
        self.cluster = cluster
        self.scheduler = scheduler
        self.task_broker = task_broker
        self.monitor = monitor

        self.task_broker.attach(self)
        self.scheduler.attach(self)
        self.monitor.attach(self)

        # self.first_task_arrive = self.env.event()

    def run(self):
        self.env.process(self.task_broker.run())
        self.env.process(self.scheduler.run())
        if not util.TIME_TEST_ON:
            # Shutdown the monitor when running the time test.
            self.env.process(self.monitor.run())

    @property
    def finished(self):
        return self.task_broker.destroyed and self.cluster.all_tasks_finished
