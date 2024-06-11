# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/5/27 15:33
# Author  : linyf49@qq.com
# File    : test1.py

import numpy as np

# s = np.array(
#     [
#         [1, 9, 8, 3],
#         [5, 4, 2, 8],
#         [9, 8, 7, 9],
#         [4, 3, 5, 2],
#         [6, 5, 9, 1],
#         [7, 6, 3, 4],
#         [2, 1, 6, 5],
#         [3, 2, 1, 7],
#         [8, 7, 4, 6],
#     ]
# )
#
# sorted_index = np.argsort(s[:, 0])[::-1]
# s_sorted = s[sorted_index]
# print(s_sorted)

# def front(a: np.ndarray) -> np.ndarray:

# ===================== K-means Test ================= #
# import numpy as np
#
#
# def entropy_weight(matrix):
#     # 标准化决策矩阵
#     norm_matrix = matrix / matrix.sum(axis=0)
#     # 计算熵值
#     k = 1.0 / np.log(matrix.shape[0])
#     entropy = -k * (norm_matrix * np.log(norm_matrix + 1e-9)).sum(axis=0)
#     # 计算权重
#     weights = (1 - entropy) / (1 - entropy).sum()
#     return weights
#
#
# def topsis(matrix, weights):
#     # 标准化决策矩阵
#     norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))
#     # 加权标准化决策矩阵
#     weighted_matrix = norm_matrix * weights
#     # 理想解和负理想解
#     ideal_solution = weighted_matrix.max(axis=0)
#     negative_ideal_solution = weighted_matrix.min(axis=0)
#     # 距离计算
#     d_pos = np.sqrt(((weighted_matrix - ideal_solution)**2).sum(axis=1))
#     d_neg = np.sqrt(((weighted_matrix - negative_ideal_solution)**2).sum(axis=1))
#     # 相对接近度
#     c = d_neg / (d_pos + d_neg)
#     return c
#
#
# # 示例数据
# s = np.array(
#     [
#         [1, 9, 8, 3],
#         [5, 4, 2, 8],
#         [9, 8, 7, 9],
#         [4, 3, 5, 2],
#         [6, 5, 9, 1],
#         [7, 6, 3, 4],
#         [2, 1, 6, 5],
#         [3, 2, 1, 7],
#         [8, 7, 4, 6],
#     ]
# )
#
# # 计算权重
# weights = entropy_weight(s)
# print("熵权法计算的权重:", weights)
#
# # 计算TOPSIS相对接近度
# c_values = topsis(s, weights)
# print("TOPSIS相对接近度:", c_values)
#
# # 按相对接近度排序
# ranked_indices = np.argsort(c_values)[::-1]
# print("排序后的方案索引:", ranked_indices)

# ===================== K-means Test ================= #

# import pandas as pd
# from sklearn import preprocessing
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# from sklearn.metrics import silhouette_score
#
# # 创建节点数据
# data = {
#     "Node1": [4, 2.5, 8],
#     "Node2": [8, 3.0, 16],
#     "Node3": [2, 2.0, 4],
#     "Node4": [6, 2.8, 12],
#     "Node5": [4, 3.2, 8],
# }
#
# # 转换为DataFrame
# df = pd.DataFrame(data, index=["cpu_num", "cpu_f", "mem"]).T
#
# # 计算CPU评分
# df["cpu"] = df["cpu_num"] * df["cpu_f"]
#
# # 选择需要标准化的列
# features = ["cpu", "mem"]
#
# # 标准化处理
# scaler = preprocessing.StandardScaler()
# df[features] = scaler.fit_transform(df[features])
#
# # 使用肘部法则确定最优K值
# inertia = []
# K_range = range(1, 4)
#
# for k in K_range:
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(df[features])
#     inertia.append(kmeans.inertia_)
#
# # 绘制肘部图
# plt.plot(K_range, inertia, marker="o")
# plt.xlabel("group num (k)")
# plt.ylabel("Inertia")
# plt.title("Find K")
# plt.show()
#
# # 假设通过肘部法则选择K=3
# k_optimal = 3
# kmeans = KMeans(n_clusters=k_optimal, random_state=42)
# df["分组"] = kmeans.fit_predict(df[features])
#
# print(df)
#
# # 评估分组效果
# sil_score = silhouette_score(df[features], df["分组"])
# print(f"轮廓系数: {sil_score}")

# ##################### best weight vector ##################
# import numpy as np
# from scipy.optimize import minimize
# np.set_printoptions(precision=2, suppress=True)
#
# def normalize(matrix):
#     # 标准化
#     return (matrix - matrix.min(axis=0)) / (matrix.max(axis=0) - matrix.min(axis=0))
#
# def entropy_weight(matrix):
#     # 计算熵权
#     m, n = matrix.shape
#     epsilon = 1e-10  # 防止log(0)
#     proportion = matrix / matrix.sum(axis=0)
#     entropy = -np.sum(proportion * np.log(proportion + epsilon), axis=0) / np.log(m)
#     diversity = 1 - entropy
#     weights = diversity / diversity.sum()
#     return weights
#
# def objective(weights, matrix, ideal, alpha=0.1):
#     # 计算目标函数
#     distances = np.sqrt(((matrix - ideal) ** 2 * weights).sum(axis=1))
#     reg_term = alpha * np.sum((weights - initial_weights) ** 2)  # 正则化项，基于初始熵权
#     return distances.sum() + reg_term
#
# def constraint(weights):
#     # 约束条件：权重之和为1
#     return np.sum(weights) - 1
#
# # 示例数据
# matrix = np.array(
#     [
#         [1, 9, 8, 3],
#         [5, 4, 2, 8],
#         [9, 8, 7, 9],
#         [4, 3, 5, 2],
#         [6, 5, 9, 1],
#         [7, 6, 3, 4],
#         [2, 1, 6, 5],
#         [3, 2, 1, 7],
#         [8, 7, 4, 6],
#     ]
# )
#
# # 1. 标准化
# norm_matrix = normalize(matrix)
#
# # 2. 计算熵权
# initial_weights = entropy_weight(norm_matrix)
# print("初始权重（熵权）:", initial_weights)
#
# # 3. 理想解
# ideal = norm_matrix.max(axis=0)
#
# # 4. 优化求解
# constraints = {'type': 'eq', 'fun': constraint}
# bounds = [(0, 1) for _ in range(matrix.shape[1])]
# result = minimize(objective, initial_weights, args=(norm_matrix, ideal), method='SLSQP', constraints=constraints, bounds=bounds)
#
# # 5. 最优权重
# optimal_weights = result.x
# print("最优权重:", optimal_weights)


# ##########################################################


import numpy as np
from scipy.optimize import minimize

np.set_printoptions(precision=2, suppress=True)
# 示例数据
data = np.array(
    [
        [1.2, 0.8, 0.6],  # 节点1: 传输时间, CPU利用率, 内存利用率
        [0.5, 0.9, 0.5],  # 节点2
        [3, 0.85, 0.7],  # 节点3
    ]
)

# 分别提取三个指标
T = data[:, 0]  # 传输时间
U_CPU = data[:, 1]  # CPU利用率
U_Memory = data[:, 2]  # 内存利用率

# 数据标准化
T_norm = (T - T.min()) / (T.max() - T.min())
U_CPU_norm = (U_CPU - U_CPU.min()) / (U_CPU.max() - U_CPU.min())
U_Memory_norm = (U_Memory - U_Memory.min()) / (U_Memory.max() - U_Memory.min())


# 构建拉格朗日目标函数
def objective(weights):
    obj_value = np.sum(
        weights[0] * T_norm
        + weights[1] * (1 - U_CPU_norm)
        + weights[2] * (1 - U_Memory_norm)
    )
    return obj_value


# 约束条件：权重之和为1
constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}

# 边界条件：每个权重在0和1之间
bounds = [(0, 1) for _ in range(3)]

# 初始权重
initial_weights = np.ones(3) / 3

# 优化求解
result = minimize(
    objective, initial_weights, method="SLSQP", constraints=constraints, bounds=bounds
)

# 最优权重
optimal_weights = result.x
print("最优权重:", optimal_weights)


# 打分函数（使用最优权重对每个节点进行打分）
def score(weights, T, U_CPU, U_Memory):
    return weights[0] * T + weights[1] * (1 - U_CPU) + weights[2] * (1 - U_Memory)


# 计算每个节点的得分
scores = score(optimal_weights, T_norm, U_CPU_norm, U_Memory_norm)
print("每个节点的得分:", scores)

# 找出得分最高的节点
best_node = np.argmin(scores)  # 最小得分对应最佳节点
print("最佳节点索引:", best_node)
