# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/13 15:49
# Author  : linyf49@qq.com
# File    : monitor.py
import json
import numpy as np
import matplotlib.pyplot as plt


class Monitor(object):
    def __init__(self, env, scheduler_name: str):
        self.env = env
        self.simulator = None
        self.cluster = None
        self.event_file = scheduler_name + "_event.txt"
        self.events = []

    def attach(self, simulator):
        self.simulator = simulator
        self.cluster = simulator.cluster

    def run(self):
        cpus = []
        mems = []
        gpus = []
        while not self.simulator.finished:
            state = {
                "timestamp": self.env.now,
                "cluster_state": self.cluster.state,
            }
            cpus.append(self.cluster.cpu_utilization)
            mems.append(self.cluster.mem_utilization)
            gpus.append(self.cluster.gpu_utilization)
            self.events.append(state)
            yield self.env.timeout(0.2)
        # final state
        state = {
            "timestamp": self.env.now,
            "cluster_state": self.cluster.state,
        }
        self.events.append(state)
        avg_utilization = {
            "avg_cpu_utilization:": "{:.2f}%".format(sum(cpus) / len(cpus)),
            "avg_mem_utilization:": "{:.2f}%".format(sum(mems) / len(mems)),
            "avg_gpu_utilization:": "{:.2f}%".format(sum(gpus) / len(gpus)),
        }
        self.events.append(avg_utilization)
        self.write_to_file()
        # self.draw(cpus, mems)

    def write_to_file(self):
        with open(self.event_file, "w") as f:
            json.dump(self.events, f, indent=4)

    @staticmethod
    def draw(cpus, mems):
        final_time = len(cpus) - 1
        tm = [i for i in range(final_time + 1)]
        x = np.arange(20, 350)
        l = plt.plot(tm, cpus, "g--", label="cpu")
        plt.plot(tm, cpus, "g-")
        plt.title("CPU Utilization")
        plt.xlabel("timestamp")
        plt.ylabel("cluster_cpu_utilization")
        plt.ylim((0, 100))
        plt.legend()
        plt.show()
