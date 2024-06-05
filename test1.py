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
import numpy as np
from scipy.optimize import minimize

def objective(weights, matrix, ideal):
    distances = np.sqrt(((matrix - ideal) ** 2 * weights).sum(axis=1))
    return distances.sum()

def constraint(weights):
    return np.sum(weights) - 1

matrix = np.array(
    [
        [1, 9, 8, 3],
        [5, 4, 2, 8],
        [9, 8, 7, 9],
        [4, 3, 5, 2],
        [6, 5, 9, 1],
        [7, 6, 3, 4],
        [2, 1, 6, 5],
        [3, 2, 1, 7],
        [8, 7, 4, 6],
    ]
)

norm_matrix = (matrix - matrix.min(axis=0)) / (matrix.max(axis=0) - matrix.min(axis=0))
ideal = norm_matrix.max(axis=0)
initial_weights = np.ones(matrix.shape[1]) / matrix.shape[1]

constraints = ({'type': 'eq', 'fun': constraint})
result = minimize(objective, initial_weights, args=(norm_matrix, ideal),
                  method='SLSQP', constraints=constraints, bounds=[(0, 1) for _ in range(matrix.shape[1])])

optimal_weights = result.x
print("最优权重:", optimal_weights)


# ##########################################################
