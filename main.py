# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 16:11
# Author  : linyf49@qq.com
# File    : main.py
from simpy import Environment
from Scheduler import rccs, lrr, bra, dics, kcss, odcs
from Infrastructure.cluster import Cluster
from simulator import Simulator
from Task.broker import Broker
from Rd import csv_reader as rd
from monitor import Monitor
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(name)s-%(lineno)s-%(levelname)s - %(message)s",
    # filemode="a",  # append at the end of Log file
    filemode="w",  # rewrite the Log file
)


def baseline_odcs(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)

    scheduler = odcs.OnlineContainerScheduling("odcs", env)
    monitor = Monitor(env, "odcs")
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    sim.run()
    env.run()
    print("average completion time of odcs:", cluster.average_completion())


def baseline_kcss(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)

    scheduler = kcss.KubernetesContainerScheduling("kcss", env)
    monitor = Monitor(env, "kcss")
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    sim.run()
    env.run()
    print("average completion time of kcss:", cluster.average_completion())


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
    monitor = Monitor(env, "lrr")
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
    monitor = Monitor(env, "bra")
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    sim.run()
    env.run()
    print("average completion time of bra:", cluster.average_completion())


def baseline_rccs(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)

    scheduler = rccs.GroupBaseContainerScheduling("rccs", env)
    monitor = Monitor(env, "rccs")
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    scheduler.make_first_level_group()
    scheduler.make_second_level_group()
    sim.run()
    env.run()
    print("average completion time:", cluster.average_completion())


def main():
    task_configs = rd.read_alibaba_task_list_csv()
    print("task data read finish.")
    node_list = rd.read_alibaba_node_list_csv()
    print("node data read finish.")

    print("baseline LRR is running...")
    baseline_lrr(task_configs, node_list)

    print("baseline DICS is running...")
    baseline_dics(task_configs, node_list)

    print("baseline BRA is running...")
    baseline_bra(task_configs, node_list)

    print("baseline KCSS is running...")
    baseline_kcss(task_configs, node_list)

    print("baseline ODCS is running...")
    baseline_odcs(task_configs, node_list)

    print("baseline RCCS is running...")
    baseline_rccs(task_configs, node_list)


if __name__ == "__main__":
    main()
