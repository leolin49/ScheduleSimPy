# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/6/13 15:49
# Author  : linyf49@qq.com
# File    : monitor.py
import json


class Monitor(object):
    def __init__(self, env):
        self.env = env
        self.simulator = None
        self.cluster = None
        self.event_file = "events.txt"
        self.events = []

    def attach(self, simulator):
        self.simulator = simulator
        self.cluster = simulator.cluster

    def run(self):
        while not self.simulator.finished:
            state = {
                "timestamp": self.env.now,
                "cluster_state": self.cluster.state,
            }
            self.events.append(state)
            yield self.env.timeout(1)
        # final state
        state = {
            "timestamp": self.env.now,
            "cluster_state": self.cluster.state,
        }
        self.events.append(state)
        self.write_to_file()

    def write_to_file(self):
        with open(self.event_file, "w") as f:
            json.dump(self.events, f, indent=4)
