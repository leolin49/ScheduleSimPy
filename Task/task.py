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


class TaskConfig(object):
    def __init__(
        self,
        task_index,
        submit_time,
        duration,
        instances_number,
        cpu,
        memory,
        disk,
        rely_data: List[Data] = None,
    ):
        """
        :param task_index: 任务唯一编号
        :param submit_time: 任务提交时间
        :param duration: 任务执行持续时间
        :param instances_number: 任务实例数量
        :param cpu: 执行任务需要的cpu
        :param memory: 执行任务需要的内存
        :param disk: 执行任务需要的磁盘
        :param rely_data: 任务执行依赖的数据
        """
        self.id = task_index
        self.submit_time = submit_time
        self.duration = duration
        self.instances_number = instances_number
        self.cpu_consume = cpu
        self.mem_consume = memory
        self.disk_consume = disk
        self.rely_data = rely_data


class Task:
    def __init__(self, env: Environment, config: TaskConfig):
        self.env = env
        self.id = config.id
        self.instances_number = config.instances_number
        self.cpu_consume = config.cpu_consume
        self.mem_consume = config.mem_consume
        self.disk_consume = config.disk_consume
        self.duration = config.duration

        self.work_node = None  # 任务被调度到哪个边缘节点
        self.process = None
        self.started = False
        self._finished = False
        self.started_timestamp = None
        self.finished_timestamp = None

        self.rely_datas = []

    def run(self):
        yield self.env.timeout(self.duration)

        self._finished = True
        self.finished_timestamp = self.env.now
        print(self.state)

    def schedule(self, node):
        self.started = True
        self.started_timestamp = self.env.now

        self.work_node = node
        self.work_node.run_task(self)
        self.process = self.env.process(self.run())

    @property
    def finished(self) -> bool:
        return self._finished

    @property
    def state(self) -> str:
        if self.finished:
            return "now:{} Task-{} is finished. begin:{}, end:{}".format(
                self.env.now, self.id, self.started_timestamp, self.finished_timestamp
            )
        return "now{} Task-{} is not begin".format(self.env.now, self.id)
