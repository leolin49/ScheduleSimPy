# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:02
# Author  : linyf49@qq.com
# File    : edge_node.py.py
from typing import List
import util


# 边缘节点基类
class EdgeNode:
    _id: int
    # CPU容量和利用率
    _cpu_capacity: float
    _cpu_utilization: float
    # 内存容量和利用率(M)
    _mem_capacity: float
    _mem_utilization: float
    # 磁盘和利用率
    _disk_capacity: float
    _disk_utilization: float
    # 网络传输带宽(Mbps)
    _bandwidth: float
    # 当前运行的容器数量
    _container_num: int
    # 标签
    _labels: List[str]

    def __init__(
        self,
        node_id: int,
        cpu_cap: float,
        mem_cap: float,
        disk_cap: float,
        bandwidth: float,
        labels=None,
    ):
        self._id = node_id
        self._cpu_capacity = cpu_cap
        self._mem_capacity = mem_cap
        self._disk_capacity = disk_cap
        self._cpu_utilization = 0
        self._mem_utilization = 0
        self._disk_utilization = 0
        self._bandwidth = bandwidth
        self._container_num = 0
        self._labels = labels

    def __str__(self):
        return "id: {}, cpu_capacity: {}, mem_capacity: {}GB, disk_capacity: {}GB, bandwidth: {}Mbps".format(
            self._id,
            self._cpu_capacity,
            self._mem_capacity / util.GB,
            self._disk_capacity / util.GB,
            self._bandwidth,
        )

    def get_id(self):
        return self._id

    def get_load_info(self) -> List[float]:
        return [
            self._id,
            self._cpu_capacity,
            self._cpu_utilization,
            self._mem_capacity,
            self._mem_utilization,
            self._disk_capacity,
            self._disk_utilization,
            self._container_num,
            self._bandwidth,
        ]

    def set_load_info(self, cpu: float, mem: float, disk: float, container_num: int):
        self._cpu_utilization = cpu
        self._mem_utilization = mem
        self._disk_utilization = disk
        self._container_num = container_num
