# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/24 20:40
# Author  : linyf49@qq.com
# File    : draw_decision.py

import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
from util import NODE_NUM, BASELINE_COLORS

directory = "./Log/log_node{}/".format(NODE_NUM)
files = [f for f in os.listdir(directory) if f.endswith("_avg_event.json")]
baselines = ["bra", "lrp", "dics", "kcss", "odcs", "rccs"]

all_timestamps = []
all_delay = []

data_by_baseline = defaultdict(list)

for file in files:
    with open(os.path.join(directory, file), "r") as f:
        data = json.load(f)[0]
        file_basename = file.split(".")[0]
        baseline, i, j = file_basename.split("_")[:3]
        data_by_baseline[baseline].append(float(data["avg_task_decision"]))

data_for_boxplot = [data_by_baseline[baseline] for baseline in baselines]
plt.figure(figsize=(10, 6))
plt.boxplot(
    data_for_boxplot,
    widths=0.3,
    patch_artist=True,
    labels=[baseline.upper() for baseline in baselines],
    boxprops=dict(facecolor="lightblue"),
    medianprops=dict(color="red"),
    whiskerprops=dict(color="black"),
    capprops=dict(color="black"),
    flierprops=dict(marker="o", color="black", markerfacecolor="black", markersize=5),
    showmeans=True,
    meanprops=dict(marker="D", markeredgecolor="black", markerfacecolor="firebrick", markersize=5),
)

plt.xlabel("Baseline", fontsize=16)
plt.xticks(fontsize=16)
plt.ylabel("Makespan (s)", fontsize=16)
plt.yticks(fontsize=16)
# plt.ylim((2.0, 3.2))

plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)

plt.show()