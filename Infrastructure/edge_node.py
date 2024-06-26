# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:02
# Author  : linyf49@qq.com
# File    : edge_node.py
from typing import List, Tuple

import util


class EdgeNodeConfig:
    def __init__(
        self,
        cpu_capacity: int,
        mem_capacity: int,
        disk_capacity: int,
        bandwidth: int,
        labels: List[str] = None,
        cpu=None,
        memory=None,
        disk=None,
    ):
        """
        :param cpu_capacity: Cpu cores number
        :param mem_capacity: Memory capacity(MB)
        :param disk_capacity: Disk capacity(MB)
        :param bandwidth: Network bandwidth(MB)
        :param labels: Hardware labels list
        :param cpu: Available cpu cores number
        :param memory: Available memory size
        :param disk: Available disk size
        """
        self.cpu_capacity = cpu_capacity
        self.mem_capacity = mem_capacity
        self.disk_capacity = disk_capacity
        self.bandwidth = bandwidth
        self.labels = labels
        self.cpu = cpu_capacity if cpu is None else cpu
        self.memory = mem_capacity if memory is None else memory
        self.disk = disk_capacity if disk is None else disk


class EdgeNode:
    def __init__(self, node_id: int, cfg: EdgeNodeConfig):
        self.id = node_id
        self.cpu_capacity = cfg.cpu_capacity
        self.cpu = cfg.cpu
        self.mem_capacity = cfg.mem_capacity
        self.mem = cfg.memory
        self.disk_capacity = cfg.disk_capacity
        self.disk = cfg.disk

        self.bandwidth = cfg.bandwidth
        self.container_num = 5
        if cfg.labels is not None:
            self.labels = cfg.labels
        else:
            self.labels = []
        self.edges = []

        self.cluster = None

    def __str__(self):
        return (
            "id: {}, "
            "cpu: {}({:.2f}% used), "
            "mem: {}GB({:.2f}% used), "
            "disk: {}GB({:.2f}% used), "
            "bandwidth: {}Mbps, "
            "running_task: {}, "
            "labels: {}".format(
                self.id,
                self.cpu_capacity,
                self.cpu_utilization,
                self.mem_capacity / util.GB,
                self.mem_utilization,
                self.disk_capacity / util.GB,
                self.disk_utilization,
                self.bandwidth,
                self.container_num,
                self.labels,
            )
        )

    def __eq__(self, other):
        return isinstance(other, EdgeNode) and other.id == self.id

    def attach(self, cluster):
        self.cluster = cluster

    @property
    def cpu_utilization(self) -> float:
        return (self.cpu_capacity - self.cpu) / self.cpu_capacity * 100

    @property
    def mem_utilization(self) -> float:
        return (self.mem_capacity - self.mem) / self.mem_capacity * 100

    @property
    def disk_utilization(self) -> float:
        return (self.disk_capacity - self.disk) / self.disk_capacity * 100

    def add_edge(self, edges: List[Tuple]):
        for e in edges:
            self.edges.append((e[0], e[1]))

    def can_run_task(self, task) -> bool:
        return (
            self.cpu >= task.cpu_consume
            and self.mem >= task.mem_consume
            # and self.disk >= task.disk_consume
        )

    def run_task(self, task):
        """
        Run a task in edge node, consume resources.
        :param task: the task object to be run
        :return:
        """
        self.cpu -= task.cpu_consume
        self.mem -= task.mem_consume
        self.disk -= task.disk_consume
        self.container_num += 1

    def stop_task(self, task):
        """
        Task end, recycle resources.
        :param task: the running task object
        :return:
        """
        self.cpu += task.cpu_consume
        self.mem += task.mem_consume
        self.disk += task.disk_consume
        self.container_num -= 1
        self.cluster.finished_task_list.append(task)
