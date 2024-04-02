# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 15:19
# Author  : linyf49@qq.com
# File    : scheduler.py.py

from Infrastructure.cluster import Cluster
from Task.task import Task


# 调度器基类
class Scheduler(object):
    def __init__(self, name: str, cluster: Cluster):
        self._name = name
        self._cluster = cluster

    def make_decision(self, task: Task):
        pass
