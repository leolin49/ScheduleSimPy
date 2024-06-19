# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 16:11
# Author  : linyf49@qq.com
# File    : main.py
from simpy import Environment
from Scheduler import PGCS4EI, lrr, bra, dics
from Infrastructure.cluster import Cluster
from simulator import Simulator
from Task.broker import Broker
from Rd import data_product as dp
from monitor import Monitor


def baseline_dics(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)

    scheduler = dics.DataIntensiveContainerScheduling("dics", env)
    monitor = Monitor(env, "dics")
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    sim.run()
    env.run()
    print("average completion time of dics:", cluster.average_completion())


def baseline_lrr(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)
    scheduler = lrr.LeastRequestedPriority("lrr", env)
    monitor = Monitor(env, 'lrr')
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    sim.run()
    env.run()
    print("average completion time of lrr:", cluster.average_completion())


def baseline_bra(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)
    scheduler = bra.BalancedResourceAllocation("bra", env)
    monitor = Monitor(env, 'bra')
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    sim.run()
    env.run()
    print("average completion time of brr:", cluster.average_completion())


def pgcs4ei(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)

    scheduler = PGCS4EI.GroupBaseContainerScheduling("pgcs4ei", env)
    monitor = Monitor(env, 'pgcs4ei')
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    scheduler.make_first_level_group()
    scheduler.make_second_level_group()
    sim.run()
    env.run()
    print("average completion time:", cluster.average_completion())


def main():
    task_configs = dp.read_task_list_csv()
    node_list = dp.read_node_list_csv()
    # baseline_dics(task_configs, node_list)
    # baseline_lrr(task_configs, node_list)
    # baseline_bra(task_configs, node_list)
    pgcs4ei(task_configs, node_list)


if __name__ == "__main__":
    main()
