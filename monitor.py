# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/13 15:49
# Author  : linyf49@qq.com
# File    : monitor.py
import json
import util


class Monitor(object):
    def __init__(self, env, scheduler_name: str):
        self.name = scheduler_name
        self.env = env
        self.simulator = None
        self.cluster = None
        self.avg_file = None
        self.event_file = "Log/" + scheduler_name + "_event.json"
        self.events = []
        self.avgs = []

    def attach(self, simulator):
        self.simulator = simulator
        self.cluster = simulator.cluster
        self.avg_file = "Log/{}_{}_{:5d}_avg_event.json".format(self.name, util.NODE_NUM, util.TASK_MUL * 8000)

    def run(self):
        cpus = []
        mems = []
        gpus = []
        while not self.simulator.finished:
            state = {
                "timestamp": self.env.now,
                # "cluster_state": self.cluster.state,
                "cpu_utilization": "{:.2f}%".format(self.cluster.cpu_utilization),
                "mem_utilization": "{:.2f}%".format(self.cluster.mem_utilization),
                "gpu_utilization": "{:.2f}%".format(self.cluster.gpu_utilization),
            }
            cpus.append(self.cluster.cpu_utilization)
            mems.append(self.cluster.mem_utilization)
            gpus.append(self.cluster.gpu_utilization)
            self.events.append(state)
            yield self.env.timeout(1)
        # self.events.append({"states": states})
        # final state
        state = {
            "avg_task_make_span": "{:.2f}".format(self.cluster.average_completion()),
            "avg_cpu_utilization": "{:.2f}%".format(sum(cpus) / len(cpus)),
            "avg_mem_utilization": "{:.2f}%".format(sum(mems) / len(mems)),
            "avg_gpu_utilization": "{:.2f}%".format(sum(gpus) / len(gpus)),
        }
        self.avgs.append(state)
        # self.events.append({"avg": state})
        self.write_to_file()
        self.write_to_file_avg()

    def write_to_file(self):
        with open(self.event_file, "w") as f:
            json.dump(self.events, f, indent=4)

    def write_to_file_avg(self):
        with open(self.avg_file, "w") as f:
            json.dump(self.avgs, f, indent=4)
