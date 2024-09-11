# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/9 20:57
# Author  : linyf49@qq.com
# File    : draw_gpu.py

import json
import matplotlib.pyplot as plt

file_paths = ['bra', 'lrr', 'dics', 'kcss','rccs']

all_timestamps = []
all_gpu_utilizations = []

for file_path in file_paths:
    with open("Log/"+file_path+"_event.json", 'r') as file:
        data = json.load(file)
        timestamps = [entry['timestamp'] for entry in data]
        gpu_utilization = [float(entry['gpu_utilization'].strip('%')) for entry in data]
        all_timestamps.append(timestamps)
        all_gpu_utilizations.append(gpu_utilization)

print(len(all_gpu_utilizations))

plt.figure(figsize=(12, 8))

for (timestamps, gpu_utilization, baseline) in zip(all_timestamps, all_gpu_utilizations, file_paths):
    plt.plot(timestamps, gpu_utilization, linestyle='-', label=baseline)

plt.title('GPU Utilization Comparison Over Time')
plt.xlabel('Timestamp (s)')
plt.ylabel('GPU Utilization (%)')
plt.xlim((5, 100))
plt.ylim((60, 100))
plt.legend()
plt.grid(True)
plt.show()
