# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/11 14:47
# Author  : linyf49@qq.com
# File    : draw_load_balance.py

import json
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

file_paths = ["bra", "lrr", "dics", "kcss", "odcs", "rccs"]
colors = ["saddlebrown", "green", "purple", "orange", "blue", "red"]

all_timestamps = []
all_lb = []
interval = 1

for file_path in file_paths:
    with open("Log/" + file_path + "_100_24000_avg_event.json", "r") as file:
        data = json.load(file)[0]
        timestamps = [i for i in range(0, 101)]
        lb = data["load_balance_state"]
        all_timestamps.append(timestamps)
        all_lb.append(lb)

plt.figure(figsize=(12, 8))

for i, (timestamps, lb, baseline) in enumerate(zip(all_timestamps, all_lb, file_paths)):
    alpha = 1 if baseline != "rccs" else 0.66

    lb_smooth = savgol_filter(lb, window_length=10, polyorder=6)

    plt.plot(
        timestamps[::interval],
        lb_smooth[::interval],
        # marker="s",
        markersize="2",
        linestyle="-",
        label=baseline.upper(),
        color=colors[i],
        alpha=alpha,
    )

# plt.title("Load Balance Comparison Over Time")
plt.xlabel("Timestamp (s)", fontsize=16)
plt.xticks(fontsize=16)
plt.ylabel("CV", fontsize=16)
plt.yticks(fontsize=16)
plt.ylim((0, 10))
plt.legend(loc="best", fontsize=20, ncol=3)
plt.grid(True)
plt.show()
