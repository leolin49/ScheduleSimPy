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
        ai_accelerators: List[str],
        ai_accelerator_num: int,
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
        :param ai_accelerators: Task request AI accelerators list(GPU, TPU, NPU).
        :param ai_accelerator_num: Task request AI accelerator number.
        :param rely_data: The data the task run needed (not used)
        """
        self.id = task_index
        self.submit_time = submit_time
        self.duration = duration
        self.transmit_time = transmit_time
        self.cpu_consume = cpu
        self.mem_consume = memory
        self.disk_consume = disk
        self.ai_accelerators = ai_accelerators
        self.ai_accelerator_num = ai_accelerator_num
        self.rely_data = rely_data

    def __str__(self):
        return (
            "id: {}, "
            "cpu_consume: {}, "
            "mem_consume: {}MB, "
            "submit_time: {:.2f}, "
            "duration: {:.2f}, "
            "ai_accelerators: {}".format(
                self.id,
                self.cpu_consume,
                self.mem_consume,
                self.submit_time,
                self.duration,
                self.ai_accelerators,
            )
        )

    def __eq__(self, other):
        return isinstance(other, Task) and other.id == self.id


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

        self.work_node_id = -1  # The edge node run the task
        self.process = None
        self.started = False
        self._finished = False
        self.started_timestamp = None
        self.finished_timestamp = None

        self.ai_accelerators = config.ai_accelerators
        self.ai_accelerator_num = config.ai_accelerator_num
        self.ai_accelerator_consume = 0
        self.rely_datas = []

    def __str__(self):
        return (
            "id: {}, "
            "cpu_consume: {}, "
            "mem_consume: {}MB, "
            "submit_time: {:.2f}, "
            "duration: {:.2f}, "
            "ai_accelerators: {}".format(
                self.id,
                self.cpu_consume,
                self.mem_consume,
                self.submit_time,
                self.duration,
                self.ai_accelerators,
            )
        )

    def run(self, node, decision_time):
        # Total time = User request time + Data transmission time + Task duration time 
        #               + (Schedule decision time)
        mul = 3.6
        addition_time = 1 if node.gpu_match(self) else mul 
        if not node.gpu_match(self):
            addition_time = mul 
        elif self.ai_accelerator_consume == self.ai_accelerator_num:
            addition_time = 1
        else:
            addition_time = 1 + (mul - 1) * (1 - self.ai_accelerator_consume / self.ai_accelerator_num);

        yield self.env.timeout(
            addition_time * self.duration + decision_time + self.transmit_time
        )
        node.stop_task(self)
        self._finished = True
        self.finished_timestamp = self.env.now
        # util.print_g(self.state)
        node.cluster.running_task_num -= 1

    def schedule(self, node, decision_time):
        self.started = True
        self.started_timestamp = self.env.now

        self.work_node_id = node.id
        node.run_task(self)
        self.env.process(self.run(node, decision_time))

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
