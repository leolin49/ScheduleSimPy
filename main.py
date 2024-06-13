# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 16:11
# Author  : linyf49@qq.com
# File    : main.py
from simpy import Environment
from Scheduler import PGCS4EI
from Infrastructure.cluster import Cluster
from simulator import Simulator
from Task.broker import Broker
import data_product as dp
from monitor import Monitor


def main():
    # ***************************** Baseline1 Start ***************************** #
    # env1 = Environment()
    # # 新建任务
    # task_configs = dp.read_task_list_csv()
    # task_broker = Broker(env1, task_configs)
    # # 新建集群及其节点
    # cluster = Cluster()
    # node_list = dp.read_node_list_csv()
    # for node in node_list:
    #     cluster.add_node(node)
    #
    # scheduler = dics.DataIntensiveContainerScheduling("dics", env1)
    # sim1 = Simulator(env1, cluster, scheduler, task_broker)
    # sim1.run()
    # env1.run()
    # print(cluster.average_completion())
    # ***************************** Baseline1 End ******************************* #

    # ***************************** Baseline2 Start ***************************** #
    env2 = Environment()
    # 新建任务
    task_configs = dp.read_task_list_csv()
    task_broker = Broker(env2, task_configs)
    # 新建集群及其节点
    cluster = Cluster()
    node_list = dp.read_node_list_csv()
    for node in node_list:
        cluster.add_node(node)

    scheduler = PGCS4EI.GroupBaseContainerScheduling("pgcs4ei", env2)
    monitor2 = Monitor(env2)
    sim2 = Simulator(env2, cluster, scheduler, task_broker, monitor2)
    scheduler.make_group()
    scheduler.make_group_2()
    sim2.run()
    env2.run()
    print("average completion time:", cluster.average_completion())
    # ***************************** Baseline2 End ******************************* #


if __name__ == "__main__":
    main()
