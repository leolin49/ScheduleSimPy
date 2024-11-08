# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/11/8 9:49
# Author  : linyf49@qq.com
# File    : count_mem.py.py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体

# 读取文件并提取每个节点的内存容量
def read_memory_capacities(file):
    ls = []
    for chunk in pd.read_csv(file, chunksize=1):
        for index, row in chunk.iterrows():
            node_id = int(row["sn"][-4:]) + 1
            cpu_capacity = int(row["cpu_milli"]) // 1000
            mem_capacity = int(row["memory_mib"])
            ls.append(mem_capacity / 1024)
    return ls

# 定义内存容量的区间
def define_memory_intervals():
    return [64*i for i in range(20)]
    # return [0, 64, 128, 256, 512, 1024, 1024*2, 1024*4]  # 例如：0-16GB, 17-32GB, ...

# 统计每个区间内出现的数量
def count_memory_in_intervals(memory_capacities, intervals):
    counts = {f"{intervals[i]+1}-{intervals[i+1]}": 0 for i in range(len(intervals)-1)}
    for capacity in memory_capacities:
        for i in range(len(intervals)-1):
            if capacity >= intervals[i] and capacity < intervals[i+1]:
                counts[f"{intervals[i]+1}-{intervals[i+1]}"] += 1
                break
    return counts

# 绘制柱状图
def plot_memory_distribution(memory_counts):
    intervals = list(memory_counts.keys())
    counts = list(memory_counts.values())

    plt.figure(figsize=(10, 8))
    bars = plt.bar(intervals, counts, color='green')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height, '%d' % int(height), ha='center', va='bottom')

    plt.xlabel('内存容量区间 (GB)')
    plt.ylabel('数量')
    plt.title('节点内存容量分布')
    plt.xticks(rotation=45)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.95)
    plt.show()

# 主函数
def main():
    filename = 'openb_node_list_gpu_node.csv'  # 假设你的文件名为node_memory.txt
    memory_capacities = read_memory_capacities(filename)
    intervals = define_memory_intervals()
    memory_counts = count_memory_in_intervals(memory_capacities, intervals)
    plot_memory_distribution(memory_counts)

if __name__ == '__main__':
    main()