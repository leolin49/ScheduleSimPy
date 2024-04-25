# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:02
# Author  : linyf49@qq.com
# File    : edge_node.py
from typing import List, Tuple

from Data.label import Label
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
        :param cpu_capacity: CPU
        :param mem_capacity: 节点内存容量（MB）
        :param disk_capacity: 节点磁盘容量（MB）
        :param bandwidth: 节点带宽（Mbps）
        :param labels: 节点标签
        :param cpu: 剩余CPU
        :param memory: 剩余内存容量
        :param disk: 剩余磁盘容量
        """
        self.cpu_capacity = cpu_capacity
        self.mem_capacity = mem_capacity
        self.disk_capacity = disk_capacity
        self.bandwidth = bandwidth
        self.labels = labels

        self.cpu = cpu_capacity if cpu is None else cpu
        self.memory = mem_capacity if memory is None else memory
        self.disk = disk_capacity if disk is None else disk


# 边缘节点基类
class EdgeNode:
    def __init__(self, node_id: int, cfg: EdgeNodeConfig):
        self.id = node_id
        self.cpu_capacity = cfg.cpu_capacity
        self.cpu = cfg.cpu_capacity
        self.mem_capacity = cfg.mem_capacity
        self.mem = cfg.mem_capacity
        self.disk_capacity = cfg.disk_capacity
        self.disk = cfg.disk_capacity

        self.bandwidth = cfg.bandwidth
        self.container_num = 0  # 节点上运行的容器数量
        if cfg.labels is not None:
            self.label = Label(set(cfg.labels))
        self.edges = []  # 节点的出边

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
                self.label
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
            and self.disk >= task.disk_consume
        )

    def run_task(self, task):
        """
        执行任务，消耗系统资源
        :param task: 待执行任务
        :return:
        """
        self.cpu -= task.cpu_consume
        self.mem -= task.mem_consume
        self.disk -= task.disk_consume
        self.container_num += 1

    def stop_task(self, task):
        """
        任务执行完成，释放系统资源
        :param task: 正在的执行任务
        :return:
        """
        self.cpu += task.cpu_consume
        self.mem += task.mem_consume
        self.disk += task.disk_consume
        self.container_num -= 1
        self.cluster.finished_task_list.append(task)
