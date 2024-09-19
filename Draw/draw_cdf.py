# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/18 22:04
# Author  : linyf49@qq.com
# File    : draw_cdf.py

import json
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from itertools import accumulate
from util import NODE_NUM, TASK_MUL, TASK_NUM, BASELINE_COLORS

baselines = ["bra", "lrp", "dics", "kcss", "odcs", "rccs"]

interval = 1

for task_mul in TASK_MUL:
    all_timestamps = []
    all_cdf = []
    for baseline in baselines:
        file_name = "Log/log_node{}/{}_{}_{}_avg_event.json".format(NODE_NUM, baseline, NODE_NUM, TASK_NUM * task_mul)
        with open(file_name, "r") as file:
            data = json.load(file)[0]
            timestamps = [i * 0.5 for i in range(0, 100)]
            cdf = list(accumulate(data['CDF']))
            all_timestamps.append(timestamps)
            all_cdf.append(cdf)

    plt.figure(figsize=(12, 8))

    for i, (timestamps, cdf, baseline) in enumerate(zip(all_timestamps, all_cdf, baselines)):
        alpha = 1 if baseline != "rccs" else 0.66

        # lb_smooth = savgol_filter(lb, window_length=16, polyorder=3)
        bp = 50
        # print(cdf)
        for idx, x in enumerate(cdf):
            if x == 1:
                bp = idx
                break
        # print(bp)

        plt.plot(
            timestamps[:bp+1:interval],
            cdf[:bp+1:interval],
            # lb_smooth[::interval],
            # marker="s",
            markersize="2",
            linestyle="-",
            linewidth=3,
            label=baseline.upper(),
            color=BASELINE_COLORS[i],
            alpha=alpha,
        )

    # plt.title("Load Balance Comparison Over Time")
    plt.xlabel("Makespan (s)", fontsize=16)
    plt.xticks(fontsize=16)
    plt.ylabel("CDF", fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylim((-0.05, 1.05))
    plt.xlim((0, 12))
    plt.legend(loc="best", fontsize=20, ncol=1)
    plt.grid(True)
    plt.show()
