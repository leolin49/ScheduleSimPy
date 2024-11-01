# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/12 21:12
# Author  : linyf49@qq.com
# File    : draw_delay.py

import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
from util import NODE_NUM, BASELINE_COLORS
import numpy as np

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
        data_by_baseline[baseline].append(float(data["avg_task_make_span"]))

data_for_boxplot = [data_by_baseline[baseline] for baseline in baselines]
print(data_for_boxplot)
plt.figure(figsize=(10, 6))
pos = [0.2 * i for i in range(6)]

bp = plt.boxplot(
    data_for_boxplot,
    widths=0.1,
    patch_artist=True,
    labels=[baseline.upper() for baseline in baselines],
    positions=pos,
    boxprops=dict(facecolor="white", linewidth=2),   # lightblue
    # boxprops=dict(visible=False),
    medianprops=dict(color="black", linewidth=2),
    whiskerprops=dict(color="black", linewidth=2),
    capprops=dict(color="black", linewidth=2),
    flierprops=dict(marker="o", color="black", markerfacecolor="black", markersize=5),
    showmeans=True,
    meanprops=dict(
        marker="D", markeredgecolor="black", markerfacecolor="lightblue", markersize=7
    ),
)

for patch, color in zip(bp['boxes'], BASELINE_COLORS):
    patch.set_facecolor(color)

FONT_SIZE = 22

plt.xlabel("Baseline", fontsize=FONT_SIZE)
plt.xticks(fontsize=FONT_SIZE)
plt.ylabel("Makespan (s)", fontsize=FONT_SIZE)
plt.yticks(fontsize=FONT_SIZE)
plt.ylim((2.2, 3.3))
plt.xlim(-0.15, 1.2)
plt.grid(True, linestyle="--", linewidth=0.5, zorder=1, axis='y')
plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.95)

# medians = [median_line.get_ydata()[0] for median_line in bp['medians']]
means = [np.mean(subdata) for subdata in data_for_boxplot]
plt.plot(pos, means, color='black', marker='o', linestyle='--', linewidth=2, dashes=(5, 5))

plt.show()
