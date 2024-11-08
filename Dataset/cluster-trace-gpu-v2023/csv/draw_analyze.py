import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
file="openb_node_list_gpu_node.csv"
counter = Counter()

for chunk in pd.read_csv(file, chunksize=1):
    for index, row in chunk.iterrows():
        node_id = int(row["sn"][-4:]) + 1
        cpu_capacity = int(row["cpu_milli"]) // 1000
        mem_capacity = int(row["memory_mib"])
        if str(row["model"]) != "nan":
            lbs = row["model"].split(",")
            cnt = [int(c) for c in str(row["gpu"]).split(",")]
            for lb in lbs:
                counter[lb] += 1

gpus = list(counter.keys())
counts = list(counter.values())

# 绘制柱状图
plt.figure(figsize=(10, 8))  # 设置图形大小

bars = plt.bar(gpus, counts, color='blue')  # 绘制柱状图

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2., height, '%d' % int(height), ha='center', va='bottom', fontsize=20)

plt.xlabel('GPU类型', fontsize=20)  # X轴标签
plt.xticks(fontsize=14)
plt.ylabel('数量', fontsize=20)  # Y轴标签
plt.yticks(fontsize=14)
plt.title('GPU的类型和数量统计图', fontsize=20)  # 图形标题
plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
plt.show()

