# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 16:15
# Author  : linyf49@qq.com
# File    : task.py
from typing import List
from simpy import Environment
from Data.data import Data
import util


class TaskConfig(object):
    def __init__(
        self,
        task_index,
        submit_time,
        duration,
        transmit_time,
        cpu,
        memory,
        disk,
        ai_accelerator: str,
        rely_data: List[Data] = None,
    ):
        """
        :param task_index: Task id
        :param submit_time: The submit time of task
        :param duration: The running time of task
        :param transmit_time: The dependent data transmit delay time
        :param cpu: Task request cpu cores number
        :param memory: Task request memory size
        :param disk: Task request disk size
        :param ai_accelerator: Task request AI accelerator(GPU, TPU, NPU)
        :param rely_data: The data the task run needed (not used)
        """
        self.id = task_index
        self.submit_time = submit_time
        self.duration = duration
        self.transmit_time = transmit_time
        self.cpu_consume = cpu
        self.mem_consume = memory
        self.disk_consume = disk
        self.ai_accelerator = ai_accelerator
        self.rely_data = rely_data


class Task:
    def __init__(self, env: Environment, config: TaskConfig):
        self.env = env
        self.id = config.id
        self.transmit_time = config.transmit_time
        self.cpu_consume = config.cpu_consume
        self.mem_consume = config.mem_consume
        self.disk_consume = config.disk_consume
        self.submit_time = config.submit_time
        self.duration = config.duration

        self.work_node = None  # The edge node run the task
        self.process = None
        self.started = False
        self._finished = False
        self.started_timestamp = None
        self.finished_timestamp = None

        self.ai_accelerator = config.ai_accelerator
        self.rely_datas = []

    def run(self, decision_time):
        # MakeSpan = Task duration time + Schedule decision time
        yield self.env.timeout(self.duration + decision_time + self.transmit_time)
        self.work_node.stop_task(self)
        self._finished = True
        self.finished_timestamp = self.env.now
        util.print_g(self.state)

    def schedule(self, node, decision_time):
        self.started = True
        self.started_timestamp = self.env.now

        self.work_node = node
        self.work_node.run_task(self)
        self.process = self.env.process(self.run(decision_time))

    @property
    def finished(self) -> bool:
        return self._finished

    @property
    def state(self) -> str:
        if self.finished:
            return "now:{} Task-{} is finished. begin:{}, end:{}, make-span:{}".format(
                self.env.now,
                self.id,
                self.started_timestamp,
                self.finished_timestamp,
                self.finished_timestamp - self.started_timestamp,
            )
        return "now:{} Task-{} duration:{} transmit:{} is not begin".format(
            self.env.now, self.id, self.duration, self.transmit_time
        )
