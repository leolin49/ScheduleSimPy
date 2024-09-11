import json
import matplotlib.pyplot as plt
import os
import numpy as np

# 读取所有 baseline 文件，文件名形如 'baseline_i_j.json'
directory = "./Log/"  # 修改为存储 JSON 文件的目录
files = [f for f in os.listdir(directory) if f.endswith("_avg_event.json")]

# 用于存储每个 baseline 的平均值和其对应的文件名 (baseline, i, j)
baselines = []
avg_task_make_span = []
avg_cpu_utilization = []
avg_mem_utilization = []
avg_gpu_utilization = []

# 用于存储不同 baseline 在不同参数组合下的数据
data_by_baseline = {}

# 读取每个文件的数据
for file in files:
    with open(os.path.join(directory, file), "r") as f:
        data = json.load(f)[0]  # 假设文件结构一致，包含一个列表并且其中有一组指标数据

        # 从文件名中提取 baseline, i, j 信息
        file_basename = file.split(".")[0]  # 去掉 .json 后缀
        baseline, i, j = file_basename.split("_")[:3]

        # 创建 baseline 的键，如果不存在则初始化
        if baseline not in data_by_baseline:
            data_by_baseline[baseline] = {
                "params": [],
                "avg_task_make_span": [],
                "avg_cpu_utilization": [],
                "avg_mem_utilization": [],
                "avg_gpu_utilization": [],
            }

        # 保存不同参数组合的 `i, j` 和对应的指标值
        data_by_baseline[baseline]["params"].append(f"|N|={i}, |C|={j}")
        data_by_baseline[baseline]["avg_task_make_span"].append(
            float(data["avg_task_make_span"])
        )
        data_by_baseline[baseline]["avg_cpu_utilization"].append(
            float(data["avg_cpu_utilization"].strip("%"))
        )
        data_by_baseline[baseline]["avg_mem_utilization"].append(
            float(data["avg_mem_utilization"].strip("%"))
        )
        data_by_baseline[baseline]["avg_gpu_utilization"].append(
            float(data["avg_gpu_utilization"].strip("%"))
        )

# 指标名称和获取对应数据的键
metrics_names = [
    "Task Make Span",
    "CPU Utilization",
    "Memory Utilization",
    "GPU Utilization",
]
t = ["Task Make Span", "CPU Utilization", "Memory Utilization"]
metrics_keys = [
    "avg_task_make_span",
    "avg_cpu_utilization",
    "avg_mem_utilization",
    "avg_gpu_utilization",
]
metrics_ylims = [(1, 3.5), (0, 100), (0, 100), (10, 100)]

# 设置柱宽和间隙
bar_width = 0.2  # 每个 baseline 的柱宽
gap_between_groups = 0.5  # 参数组合之间的间隙

# 分别为每个指标绘制图表，将不同参数组合放在一起比较
for metric_name, metric_key, metrics_ylim in zip(
    metrics_names, metrics_keys, metrics_ylims
):
    if metric_name in t:
        continue
    plt.figure(figsize=(12, 8))

    # 计算每个参数组合的起始位置，插入间隙
    num_params = len(next(iter(data_by_baseline.values()))["params"])
    index = np.arange(num_params) * (
        bar_width * len(data_by_baseline) + gap_between_groups
    )

    # 为每个 baseline 绘制柱状图
    colors = ["brown", "green", "red", "blue", "orange", "purple"]
    for idx, (baseline, data) in enumerate(data_by_baseline.items()):
        plt.bar(
            index + idx * bar_width,
            data[metric_key],
            bar_width,
            color=colors[idx],
            label=baseline.upper(),
            hatch="",
            alpha=1,
        )

    # 设置标签和标题
    plt.xlabel("Parameter Combination (|N|, |C|)", fontsize=15)
    plt.ylabel(f"{metric_name} (%)", fontsize=15)
    plt.title(
        f"Comparison of {metric_name} Across Baselines for Different Parameters",
        fontsize=15,
    )

    # 设置 x 轴的刻度
    plt.xticks(
        index + (len(data_by_baseline) * bar_width) / 2,
        next(iter(data_by_baseline.values()))["params"],
        rotation=45,
        ha="right",
        fontsize=12,
    )
    plt.yticks(fontsize=12)

    # 显示图例
    plt.legend(loc="upper left", fontsize="16", ncol=6)
    plt.ylim(metrics_ylim)
    # 调整布局，避免标签重叠
    plt.tight_layout()
    # plt.grid(True)
    # 显示图形
    plt.show()
