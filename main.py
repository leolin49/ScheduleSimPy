# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 16:11
# Author  : linyf49@qq.com
# File    : main.py.py

from Scheduler import dics
from Infrastructure.cluster import Cluster
from Infrastructure.edge_node import EdgeNode
from Random import random_infrastructure as rdi
from task import Task
import util


def main():
    task = Task()
    cluster = Cluster()

    node_list = rdi.random_edge_node_list(10000)
    for node in node_list:
        cluster.add_node(node)
        # print(node.__str__())

    scheduler = dics.DataIntensiveContainerScheduling("dics", cluster)
    util.run_with_time(scheduler.get_best_node)


if __name__ == "__main__":
    main()
