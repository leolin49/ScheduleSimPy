# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/11 14:47
# Author  : linyf49@qq.com
# File    : draw_load_balance.py

import json
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from util import NODE_NUM, TASK_MUL, TASK_NUM, BASELINE_COLORS

baselines = ["bra", "lrp", "dics", "kcss", "odcs", "rccs"]

interval = 1

for task_mul in TASK_MUL:
    all_timestamps = []
    all_lb = []
    for baseline in baselines:
        file_name = "Log/log_node{}/{}_{}_{:02d}_avg_event.json".format(NODE_NUM, baseline, NODE_NUM, task_mul)
        with open(file_name, "r") as file:
            data = json.load(file)[0]
            timestamps = [i for i in range(0, 101)]
            lb = data["load_balance_state"]
            all_timestamps.append(timestamps)
            all_lb.append(lb)

    plt.figure(figsize=(12, 8))

    for i, (timestamps, lb, baseline) in enumerate(zip(all_timestamps, all_lb, baselines)):
        alpha = 1 if baseline != "rccs" else 0.66

        lb_smooth = savgol_filter(lb, window_length=16, polyorder=5)

        plt.plot(
            timestamps[::interval],
            lb_smooth[::interval],
            # marker="s",
            markersize="2",
            linestyle="-",
            linewidth=2.0,
            label=baseline.upper(),
            color=BASELINE_COLORS[i],
            alpha=alpha,
        )

    # plt.title("Load Balance Comparison Over Time")
    plt.xlabel("Timestamp (s)", fontsize=16)
    plt.xticks(fontsize=16)
    plt.ylabel("Coefficient of Variation", fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylim((0, 7))
    plt.legend(loc="best", fontsize=18, ncol=1)
    plt.grid(True)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)

    plt.show()
