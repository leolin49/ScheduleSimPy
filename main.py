# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/28 16:11
# Author  : linyf49@qq.com
# File    : main.py
import platform
import sys
import time
import random
from simpy import Environment

import Rd.csv_reader
import util
from Scheduler import rccs, lrp, bra, dics, kcss, odcs
from Infrastructure.cluster import Cluster
from simulator import Simulator
from Task.broker import Broker
from Rd.csv_reader import ALIBABA_TASK_LIST, ALIBABA_NODE_LIST
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


def baseline_lrp(task_configs, node_list):
    env = Environment()
    task_broker = Broker(env, task_configs)
    cluster = Cluster()
    for node in node_list:
        cluster.add_node(node)
    scheduler = lrp.LeastRequestedPriority("lrp", env)
    monitor = Monitor(env, "lrp")
    sim = Simulator(env, cluster, scheduler, task_broker, monitor)
    sim.run()
    env.run()
    print("average completion time of lrp:", cluster.average_completion())


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


def get_node_list(node_num: int, node_mul: int):
    res = []
    if len(ALIBABA_NODE_LIST) <= node_num:
        print(
            "No enough sample node: total: {}, require: {}",
            len(ALIBABA_NODE_LIST),
            node_num,
        )
        exit(0)
    for _ in range(node_mul):
        if util.RANDOM_NODE_SAMPLE:
            res.extend(random.sample(ALIBABA_NODE_LIST, node_num))
        else:
            res.extend(ALIBABA_NODE_LIST[:node_num])
    for i, node in enumerate(res):
        node.id = i + 1
    return res


def get_task_configs(task_num: int, task_mul: int):
    res = []
    if len(ALIBABA_TASK_LIST) <= task_num:
        print(
            "No enough sample task: total: {}, require: {}",
            len(ALIBABA_TASK_LIST),
            task_num,
        )
        exit(0)
    tmp = random.sample(ALIBABA_TASK_LIST, task_num)
    for _ in range(task_mul):
        res.extend(random.sample(ALIBABA_TASK_LIST, task_num))
        # res.extend(tmp)
    res.sort(key=lambda x: x.submit_time)
    return res


def run_with_config(node_list, task_configs):
    print(
        "Experimental Parameters: Node: {}, Task: {}".format(
            len(node_list), len(task_configs)
        )
    )

    print("Baseline LRP is running...")
    baseline_lrp(task_configs, node_list)

    print("Baseline DICS is running...")
    baseline_dics(task_configs, node_list)

    print("Baseline BRA is running...")
    baseline_bra(task_configs, node_list)

    print("Baseline KCSS is running...")
    baseline_kcss(task_configs, node_list)

    print("Baseline ODCS is running...")
    baseline_odcs(task_configs, node_list)

    print("Baseline RCCS is running...")
    baseline_rccs(task_configs, node_list)


def read_dataset_alibaba():
    print("node data read begin...")
    Rd.csv_reader.read_alibaba_node_list_csv(
        "Dataset/cluster-trace-gpu-v2023/csv/openb_node_list_gpu_node.csv",
    )
    print("node data read finish...")
    print("task data read begin...")
    Rd.csv_reader.read_alibaba_task_list_csv(
        "Dataset/cluster-trace-gpu-v2023/csv/openb_pod_list_gpuspec33.csv",
    )
    print("task data read finish...")


def main():
    print("*========================================================================*")
    print(
        "Experimental Time:\t{}\nPlatform Info:\t{}\nPython Version:\t{}\n".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            platform.platform(),
            sys.version,
        )
    )
    print("*========================================================================*")
    read_dataset_alibaba()

    node_list = get_node_list(util.NODE_NUM, util.NODE_MUL)
    for task_mul in util.TASK_MUL:
        task_configs = get_task_configs(util.TASK_NUM, task_mul)
        run_with_config(node_list, task_configs)
        if util.TIME_TEST_ON:
            break


if __name__ == "__main__":
    main()
