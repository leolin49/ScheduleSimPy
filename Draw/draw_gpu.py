# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/9 20:57
# Author  : linyf49@qq.com
# File    : draw_gpu.py

import json
import matplotlib.pyplot as plt

interval = 1
file_paths = ["bra", "lrr", "dics", "kcss", "odcs", "rccs"]
colors = ["saddlebrown", "green", "purple", "orange", "blue", "red"]

all_timestamps = []
all_gpu_utilizations = []

for file_path in file_paths:
    with open("Log/" + file_path + "_event.json", "r") as file:
        data = json.load(file)
        timestamps = [entry["timestamp"] for entry in data]
        gpu_utilization = [float(entry["gpu_utilization"].strip("%")) for entry in data]
        all_timestamps.append(timestamps)
        all_gpu_utilizations.append(gpu_utilization)

plt.figure(figsize=(12, 8))

for i, (timestamps, gpu_utilization, baseline) in enumerate(
    zip(all_timestamps, all_gpu_utilizations, file_paths)
):
    alpha = 1
    if baseline != "rccs":
        alpha = 0.7
    plt.plot(
        timestamps[::interval],
        gpu_utilization[::interval],
        linestyle="-",
        label=baseline.upper(),
        color=colors[i],
        alpha=alpha,
    )

plt.title("GPU Utilization Comparison Over Time")
plt.xlabel("Timestamp (s)")
plt.ylabel("GPU Utilization (%)")
plt.xlim((1, 100))
plt.ylim((0, 100))
plt.legend(loc="best", fontsize="16", ncol=3)
plt.grid(True)
plt.show()
