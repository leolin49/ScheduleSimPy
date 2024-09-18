# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/13 9:51
# Author  : linyf49@qq.com
# File    : draw_gpu.py

import json
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from util import NODE_NUM, BASELINE_COLORS

interval = 1
baselines = ["bra", "lrp", "dics", "kcss", "odcs", "rccs"]

all_timestamps = []
all_gpu_utilizations = []

for baseline in baselines:
    file_path = "Log/log_node{}/{}_event.json".format(NODE_NUM, baseline)
    with open(file_path) as file:
        data = json.load(file)
        timestamps = [entry["timestamp"] for entry in data]
        gpu_utilization = [float(entry["gpu_utilization"].strip("%")) for entry in data]
        all_timestamps.append(timestamps)
        all_gpu_utilizations.append(gpu_utilization)

plt.figure(figsize=(12, 8))

for i, (timestamps, gpu_utilization, baseline) in enumerate(
        zip(all_timestamps, all_gpu_utilizations, baselines)
):
    alpha = 1 if baseline == "rccs" else 0.7

    gpu_utilization_smooth = savgol_filter(gpu_utilization, window_length=16, polyorder=4)

    plt.plot(
        timestamps[::interval],
        gpu_utilization_smooth[::interval],
        linestyle="-",
        label=baseline.upper(),
        color=BASELINE_COLORS[i],
        alpha=alpha,
    )

# plt.title("GPU Utilization Comparison Over Time")
plt.xlabel("Timestamp (s)", fontsize=16)
plt.xticks(fontsize=16)
plt.ylabel("GPU Utilization (%)", fontsize=16)
plt.yticks(fontsize=16)
plt.xlim((0, 100))
plt.ylim((0, 100))
plt.legend(loc="lower right", fontsize=20, ncol=1)
plt.grid(True)
plt.show()
