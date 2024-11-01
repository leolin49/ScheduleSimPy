# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/10/29 21:12
# Author  : linyf49@qq.com
# File    : draw_delay.py

import json
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.signal import savgol_filter

import util
from util import NODE_NUM, TASK_MUL, TASK_NUM, BASELINE_COLORS

baselines = ["bra", "lrp", "dics", "kcss", "odcs", "rccs"]

interval = 1

data_by_baseline = defaultdict(list)

for task_mul in TASK_MUL[:1]:
    all_timestamps = []
    all_lb = []
    for baseline in baselines:
        file_name = "Log/log_node{}/{}_{}_{:02d}_avg_event.json".format(
            NODE_NUM, baseline, NODE_NUM, task_mul
        )
        with open(file_name, "r") as file:
            data = json.load(file)[0]
            ms = data["all_make_span"]
            data_by_baseline[baseline] = ms

    plt.figure(figsize=(10, 6))

    data_for_boxplot = [data_by_baseline[baseline] for baseline in baselines]
    pos = [0.2 * i for i in range(6)]
    plt.boxplot(
        data_for_boxplot,
        widths=0.1,
        patch_artist=True,
        labels=[baseline.upper() for baseline in baselines],
        positions=pos,
        boxprops=dict(facecolor="white"),  # lightblue
        # boxprops=dict(visible=False),
        medianprops=dict(color="red"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
        flierprops=dict(marker="o", color="black", markerfacecolor="black", markersize=5),
        showmeans=True,
        meanprops=dict(
            marker="D", markeredgecolor="black", markerfacecolor="firebrick", markersize=5
        ),
    )

    FONT_SIZE = 22

    plt.xlabel("Baseline", fontsize=FONT_SIZE)
    plt.xticks(fontsize=FONT_SIZE)
    plt.ylabel("Makespan (s)", fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    # plt.ylim((2.2, 3.3))
    plt.xlim(-0.15, 1.2)

    plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.95)

    plt.show()
