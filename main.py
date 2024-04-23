# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 16:11
# Author  : linyf49@qq.com
# File    : main.py.py
import simpy
from simpy import Environment

from Scheduler import dics
from Infrastructure.cluster import Cluster
from Random import random as rd
from simulator import Simulator
from Task.broker import Broker


def main():
    # ***************************** Baseline1 Start ***************************** #
    env1 = Environment()
    # 新建任务
    task_configs = rd.random_task_list(env1, 10)
    # task_configs = rd.test_task(env1)
    task_broker = Broker(env1, task_configs)
    # 新建集群及其节点
    cluster = Cluster()
    node_list = rd.random_edge_node_list(1000)
    for node in node_list:
        cluster.add_node(node)
    scheduler = dics.DataIntensiveContainerScheduling("dics", env1)
    sim1 = Simulator(env1, cluster, scheduler, task_broker)
    sim1.run()
    env1.run()
    print(cluster.average_completion())
    # ***************************** Baseline1 End ***************************** #


if __name__ == "__main__":
    main()
