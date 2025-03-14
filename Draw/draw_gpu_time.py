# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/29 21:52
# Author  : linyf49@qq.com
# File    : draw_gpu_time.py

import json

import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

import util
from util import NODE_NUM, TASK_MUL, TASK_NUM, BASELINE_COLORS, BASELINE_NAME

interval = 2

for task_mul in TASK_MUL:
    all_timestamps = []
    all_gpus = []
    for baseline in BASELINE_NAME:
        file_name = "Log/log_node{}/{}_{}_{:02d}_avg_event.json".format(
            NODE_NUM, baseline, NODE_NUM, task_mul
        )
        with open(file_name, "r") as file:
            data = json.load(file)[0]
            timestamps = [i * 0.5 for i in range(len(data["gpus"]))]
            all_timestamps.append(timestamps)
            all_gpus.append(data["gpus"])

    plt.figure(figsize=(12, 8))

    for i, (timestamps, gpus, baseline) in enumerate(
        zip(all_timestamps, all_gpus, BASELINE_NAME)
    ):
        # alpha = 1 if baseline != "rccs" else 0.66
        alpha = 1
        gpus_smooth = savgol_filter(gpus, window_length=16, polyorder=10)
        plt.plot(
            timestamps[::interval],
            gpus[::interval],
            # gpus_smooth[::interval],
            # marker="*",
            markersize="5",
            linestyle="-",
            linewidth=1.5,
            label=baseline.upper(),
            color=BASELINE_COLORS[i],
            alpha=alpha,
        )

    FONT_SIZE = 24
    # plt.title("Load Balance Comparison Over Time")
    plt.xlabel("Timestamp (s)", fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.ylabel("GPU Utilization (%)", fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.ylim((40, 100))
    plt.xlim((0, util.TIME_RANGE))
    plt.legend(loc="lower right", fontsize=FONT_SIZE, ncol=3)
    plt.grid(True)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)

    plt.show()
