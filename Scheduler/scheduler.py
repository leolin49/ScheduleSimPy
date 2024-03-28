# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:19
# Author  : linyf49@qq.com
# File    : scheduler.py.py

from Infrastructure.cluster import Cluster
from task import Task


# 调度器基类
class Scheduler:
    _name: str
    _cluster: Cluster  # 调度器所管理的边缘集群

    def __init__(self, name: str, cluster: Cluster):
        self._name = name
        self._cluster = cluster

    def get_best_node(self, task: Task):
        pass
