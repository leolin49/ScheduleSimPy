# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:02
# Author  : linyf49@qq.com
# File    : edge_node.py
from typing import List, Tuple
from collections import Counter

import util


class EdgeNodeConfig:
    def __init__(
        self,
        cpu_capacity: int,
        mem_capacity: int,
        disk_capacity: int,
        gpu_capacity: int,
        bandwidth: int,
        labels: List[str] = None,
        counts: List[int] = None,
        cpu=None,
        memory=None,
        disk=None,
        gpu=None,
    ):
        """
        :param cpu_capacity: Cpu cores number
        :param mem_capacity: Memory capacity(MB)
        :param disk_capacity: Disk capacity(MB)
        :param gpu_capacity: GPU cores number
        :param bandwidth: Network bandwidth(MB)
        :param labels: Hardware labels list
        :param counts: The count of Hardware in labels
        :param cpu: Available cpu cores number
        :param memory: Available memory size
        :param disk: Available disk size
        :param gpu: Available gpu cores number
        """
        assert len(labels) == len(counts)
        self.cpu_capacity = cpu_capacity
        self.mem_capacity = mem_capacity
        self.disk_capacity = disk_capacity
        self.bandwidth = bandwidth
        self.gpu_capacity = gpu_capacity
        self.labels = labels
        self.counts = counts
        self.cpu = cpu_capacity if cpu is None else cpu
        self.memory = mem_capacity if memory is None else memory
        self.disk = disk_capacity if disk is None else disk
        self.gpu = gpu_capacity if gpu is None else gpu


class EdgeNode:
    def __init__(self, node_id: int, cfg: EdgeNodeConfig):
        self.id = node_id
        self.cpu_capacity = cfg.cpu_capacity
        self.cpu = cfg.cpu
        self.mem_capacity = cfg.mem_capacity
        self.mem = cfg.memory
        self.disk_capacity = cfg.disk_capacity
        self.disk = cfg.disk

        self.gpu_capacity = cfg.gpu_capacity
        self.gpu = cfg.gpu

        self.bandwidth = cfg.bandwidth
        self.container_num = 5
        self.labels = []
        self.labels_count = Counter()
        if cfg.labels is not None:
            for i, label in enumerate(cfg.labels):
                self.labels.append(label)
                self.labels_count[label] = cfg.counts[i]
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
                self.labels_count,
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
    
    @property
    def gpu_utilization(self) -> float:
        return (self.gpu_capacity - self.gpu) / self.gpu_capacity * 100

    def add_edge(self, edges: List[Tuple]):
        for e in edges:
            self.edges.append((e[0], e[1]))

    def can_run_task(self, task) -> bool:
        return (
            self.cpu >= task.cpu_consume
            and self.mem >= task.mem_consume
            and self.gpu >= task.ai_accelerator_num
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
        self.gpu -= task.ai_accelerator_num
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
        self.gpu += task.ai_accelerator_num
        self.container_num -= 1
        self.cluster.finished_task_list.append(task)
