# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/5/28 15:49
# Author  : linyf49@qq.com
# File    : PGCS4EI.py.py
"""
step1. Use K-means to decide each node in which group.
step2. Maintain the hash_map for group_id and node_ids.

CPU(Central Processing Unit)
GPU(Graphics Processing Unit)
TPU(Tensor Processing Unit)
NPU(Neural network Processing Unit)
"""

import pandas as pd
import numpy as np
from scipy.optimize import minimize
from sklearn import preprocessing
from sklearn.cluster import KMeans

import util
from Task.task import Task
from Scheduler.scheduler import Scheduler
from Infrastructure.edge_node import EdgeNode

np.set_printoptions(precision=2, suppress=True)


class GroupBaseContainerScheduling(Scheduler):
    def __init__(self, name: str, env):
        super(GroupBaseContainerScheduling, self).__init__(name, env)
        self.groups = dict()
        self.groups2 = dict()  # {'group_id': {'ai_label': [node_id1, node_id2]}}
        self.groups_min = dict()  # min(CPU,MEM) in one group

    def make_first_level_group(self):
        data = []
        for node in self.cluster.node_list:
            data.append(
                [
                    node.id,
                    node.cpu_capacity,
                    node.mem_capacity,
                    node.disk_capacity,
                    node.bandwidth,
                ]
            )
        df = pd.DataFrame(data, columns=["id", "cpu", "mem", "disk", "band"])
        df_original = df.copy()
        features = ["cpu", "mem"]

        # Normalize.
        scaler = preprocessing.MinMaxScaler()
        df[features] = scaler.fit_transform(df[features])

        k_optimal = 3
        # Custom K-means initial centroids.
        # custom_centroids = df_original.loc[[59, 89, 99], features].values
        # kmeans = KMeans(n_clusters=k_optimal, init=custom_centroids, n_init=1, random_state=42)
        kmeans = KMeans(n_clusters=k_optimal, random_state=42)
        df["cluster"] = kmeans.fit_predict(df[features])

        cluster_groups = df.groupby("cluster")
        worst_machines = []
        for cluster_id, group in cluster_groups:
            worst_machine = group.sort_values(by=["cpu", "mem"]).iloc[0]
            worst_machines.append(
                (cluster_id, worst_machine["cpu"], worst_machine["mem"])
            )
        worst_machines.sort(key=lambda x: (x[1], x[2]))
        group_ids = {
            cluster_id: idx + 1 for idx, (cluster_id, _, _) in enumerate(worst_machines)
        }

        df["group_id"] = df["cluster"].map(group_ids)
        df_original["group_id"] = df["group_id"]
        for index, row in df_original.iterrows():
            # print(
            #     f"ID: {row['id']}, "
            #     f"CPU: {row['cpu']}, "
            #     f"Mem: {row['mem']}MB, "
            #     f"Disk: {row['disk']}MB, "
            #     f"Bandwidth: {row['band']}Mbps, "
            #     f"Group: {row['group_id']}"
            # )
            group_id = row["group_id"]
            node_id = row["id"]
            if group_id not in self.groups:
                self.groups[group_id] = []
            self.groups[group_id].append(node_id)
        # print(self.groups)

        for group_id, node_ids in self.groups.items():
            min_id = min(
                node_ids,
                key=lambda idx: (
                    self.cluster.node_list[idx - 1].cpu_capacity,
                    self.cluster.node_list[idx - 1].mem_capacity,
                ),
            )
            self.groups_min[group_id] = min_id
            # print(group_id, self.cluster.node_list[min_id - 1])
        util.print_g("First level group finish...")

    def make_second_level_group(self):
        for group_id, node_ids in self.groups.items():
            self.groups2[group_id] = dict()
            for node_id in node_ids:
                node = self.cluster.node_list[node_id - 1]
                for label in node.labels:
                    if label in util.AI_LABEL:
                        if label not in self.groups2[group_id]:
                            self.groups2[group_id][label] = []
                        self.groups2[group_id][label].append(node_id)
        util.print_g("Second level group finish...")

    @staticmethod
    def can_run(task: Task, node: EdgeNode) -> bool:
        return (
            task.cpu_consume <= node.cpu_capacity
            and task.mem_consume <= node.mem_capacity
        )

    @staticmethod
    def objective(weights, matrix, ideal, alpha=0.1):
        distances = np.sqrt(((matrix - ideal) ** 2 * weights).sum(axis=1))
        # reg_term = alpha * np.sum(weights**2)
        # return distances.sum() + reg_term
        return distances.sum()

    @staticmethod
    def constraint(weights):
        return np.sum(weights) - 1

    @staticmethod
    def normalize_matrix(m):
        min_vals = m.min(axis=0)
        max_vals = m.max(axis=0)
        ranges = max_vals - min_vals
        ranges[ranges == 0] = 1  # ranges = 1 if ranges == 0
        norm = (m - min_vals) / ranges
        return norm

    def make_decision(self, task: Task, clock) -> int:
        # 1. find the first-level groups
        gid = -1
        for k, v in self.groups_min.items():
            # TODO FIXED ME
            if k == 1:
                continue
            if self.can_run(task, self.cluster.node_list[v]):
                gid = k
                break
        if gid == -1:
            util.print_r("first-level, not any node can run the task:", task)
            return -1
        # 2. find the second-level groups
        node_ids = []
        for k, v in self.groups2[gid].items():
            if k == task.ai_accelerator:
                node_ids = v
        if len(node_ids) == 0:
            util.print_r(
                "second-level, not any node in group-{} run the task-{}, need {}:".format(
                    gid, task.id, task.ai_accelerator
                )
            )
            return -1
        # 3. find the optimal_weights
        info = []
        for node_id in node_ids:
            node = self.cluster.node_list[node_id - 1]
            t = [1 / task.transmit_time, node.cpu, node.mem]
            info.append(t)

        matrix = np.array(info)
        norm_matrix = self.normalize_matrix(matrix)
        ideal = norm_matrix.max(axis=0)
        initial_weights = np.ones(matrix.shape[1]) / matrix.shape[1]
        constraints = {"type": "eq", "fun": self.constraint}
        result = minimize(
            self.objective,
            initial_weights,
            args=(norm_matrix, ideal),
            method="SLSQP",
            constraints=constraints,
            bounds=[(0.1, 0.9) for _ in range(matrix.shape[1])],
        )

        optimal_weights = result.x
        # optimal_weights = [0.33, 0.33, 0.33]
        # print("optimal_weights:", optimal_weights)

        # 4. VIKOR
        # Weighted Normalization
        # print(norm_matrix)
        weight_norm_matrix = norm_matrix * optimal_weights
        # Ideal solution and negative-ideal solution
        f_star = weight_norm_matrix.max(axis=0)
        f_minus = weight_norm_matrix.min(axis=0)
        # Calculate 'S' value and 'R' value
        S = np.zeros(matrix.shape[0])
        R = np.zeros(matrix.shape[0])
        for i in range(matrix.shape[0]):
            S[i] = np.sum(
                optimal_weights
                * (f_star - weight_norm_matrix[i])
                / (f_star - f_minus + 1e-6)
            )
            R[i] = np.max(
                optimal_weights
                * (f_star - weight_norm_matrix[i])
                / (f_star - f_minus + 1e-6)
            )
        # S = np.sum(optimal_weights * (f_star - weight_norm_matrix) / (f_star - f_minus), axis=1)
        # R = np.max(optimal_weights * (f_star - weight_norm_matrix) / (f_star - f_minus), axis=1)
        # Calculate 'Q' value
        v = 0.5
        S_star = np.min(S)
        S_minus = np.max(S)
        R_star = np.min(R)
        R_minus = np.max(R)

        Q = np.zeros(matrix.shape[0])
        for i in range(matrix.shape[0]):
            Q[i] = v * (S[i] - S_star) / (S_minus - S_star + 1e-6) + (1 - v) * (
                R[i] - R_star
            ) / (R_minus - R_star + 1e-6)

        # print("S:", S)
        # print("R:", R)

        ranking_indices = np.argsort(Q)
        ranked_ids = [node_ids[i] for i in ranking_indices]
        return ranked_ids[0]


"""
"""
# TODO list
# 1. 除数为0
# 2. 调度失败
