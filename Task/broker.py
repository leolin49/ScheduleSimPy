# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/3 15:09
# Author  : linyf49@qq.com
# File    : broker.py
from Task.task import Task


class Broker(object):
    def __init__(self, env, job_configs):
        self.env = env
        self.simulator = None
        self.cluster = None
        self.destroyed = False
        self.job_configs = job_configs

    def attach(self, simulator):
        self.simulator = simulator
        self.cluster = simulator.cluster

    def run(self):
        for job_config in self.job_configs:
            assert job_config.submit_time >= self.env.now
            yield self.env.timeout(job_config.submit_time - self.env.now)
            task = Task(self.env, job_config)
            print(
                "now:{}, task-{} is added to cluster, {}".format(
                    self.env.now, task.id, task.state
                )
            )
            self.cluster.add_task(task)
        self.destroyed = True
