# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/5/28 15:49
# Author  : linyf49@qq.com
# File    : rccs.py
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
from collections import defaultdict
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable

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
        self.groups_min = (
            dict()
        )  # min(CPU,MEM) in one group {'group_id': 'min_node_id'}

        self.BWM_WEIGHT = self.__best_worst_method_get_weights()
        print("Best-Worst Method Weights = ", self.BWM_WEIGHT)

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

        k_optimal = util.GROUP_COUNT
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
            print(group_id, self.cluster.node_list[min_id - 1])
        print("First level group finish...")

    def make_second_level_group(self):
        for group_id, node_ids in self.groups.items():
            self.groups2[group_id] = defaultdict(list)
            for node_id in node_ids:
                node = self.cluster.node_list[node_id - 1]
                for label in node.labels:
                    if label in util.AI_LABEL:
                        self.groups2[group_id][label].append(node_id)
            print(
                "group_id: {}, second group keys: {}".format(
                    group_id, self.groups2[group_id].keys()
                )
            )
        print("Second level group finish...")

    def __find_in_first_group(self, task: Task) -> int:
        # 1. find the first-level groups
        for gid, node_id in self.groups_min.items():
            if self.can_run(task, self.cluster.node_list[node_id]):
                return gid
        return -1

    def __find_in_second_group(self, gid: int, task: Task, ai_match: bool):
        # 2. find the second-level groups
        node_ids = []
        if not ai_match:
            for v in self.groups2[gid].values():
                node_ids.extend(v)
        else:
            for k, v in self.groups2[gid].items():
                if k in task.ai_accelerators:
                    node_ids.extend(v)
        return node_ids

    def __vikor(self, node_ids, task) -> int:
        # 3. find the optimal_weights
        info = []
        for node_id in node_ids:
            node = self.cluster.node_list[node_id - 1]
            # t = [1 / task.transmit_time, node.cpu, node.mem]
            t = [1 / task.transmit_time, node.gpu, node.cpu, node.mem]
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
        # optimal_weights = np.ones(matrix.shape[1]) / matrix.shape[1]
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
        node_id = -1
        for nid in ranked_ids:
            ok, err = self.cluster.node_list[nid - 1].can_run_task(task)
            if ok:
                node_id = nid
                break
        return node_id

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

    @staticmethod
    def __fuzzy_best_worst_method_get_weights():
        return  # FIXED ME
        lv = []
        lv.append([0, 0, 0, 0])
        lv.append([0, 1, 1, 1])  # Equally importance
        lv.append([0, 2 / 3, 1, 3 / 2])  # Weakly important
        lv.append([0, 3 / 2, 2, 5 / 2])  # Fairly Important
        lv.append([0, 5 / 2, 3, 7 / 2])  # Very important
        lv.append([0, 7 / 2, 4, 9 / 2])  # Absolutely important
        # GPU > Delay > MEM > CPU
        # best_idx = 1(GPU) | worst_idx = 3(CPU)
        a = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0],
            [0, 2, 1, 4, 3],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 2, 0],
        ]

        def GMIR(tp) -> float:
            return (tp[0] + tp[1] * 4 + tp[2]) / 6

        problem = LpProblem("Fuzzy_BWM_Objective", LpMinimize)
        ks = LpVariable("ks", lowBound=0)
        problem += ks, "Objective"
        # w1 = (l1,m1,u1)
        w = LpVariable.dicts(
            "w", ((i, j) for i in range(1, 5) for j in range(1, 4)), lowBound=0
        )

        bi = 1
        wi = 3
        low, mid, hig = 1, 2, 3
        for i in range(1, len(a)):
            if i == bi:
                continue
            problem += (
                w[(bi, low)] - lv[a[bi][i]][low] * w[(i, hig)] <= ks * w[(i, hig)]
            )
            problem += (
                w[(bi, low)] - lv[a[bi][i]][low] * w[(i, hig)] >= -ks * w[(i, hig)]
            )
            problem += (
                w[(bi, mid)] - lv[a[bi][i]][mid] * w[(i, mid)] <= ks * w[(i, mid)]
            )
            problem += (
                w[(bi, mid)] - lv[a[bi][i]][mid] * w[(i, mid)] >= -ks * w[(i, mid)]
            )
            problem += (
                w[(bi, hig)] - lv[a[bi][i]][hig] * w[(i, low)] <= ks * w[(i, low)]
            )
            problem += (
                w[(bi, hig)] - lv[a[bi][i]][hig] * w[(i, low)] >= -ks * w[(i, low)]
            )
        for i in range(1, len(a)):
            if i == bi or i == wi:
                continue
            problem += (
                w[(i, low)] - lv[a[i][wi]][low] * w[(wi, hig)] <= ks * w[(wi, hig)]
            )
            problem += (
                w[(i, low)] - lv[a[i][wi]][low] * w[(wi, hig)] >= -ks * w[(wi, hig)]
            )
            problem += (
                w[(i, mid)] - lv[a[i][wi]][mid] * w[(wi, mid)] <= ks * w[(wi, mid)]
            )
            problem += (
                w[(i, mid)] - lv[a[i][wi]][mid] * w[(wi, mid)] >= -ks * w[(wi, mid)]
            )
            problem += (
                w[(i, hig)] - lv[a[i][wi]][hig] * w[(wi, low)] <= ks * w[(wi, low)]
            )
            problem += (
                w[(i, hig)] - lv[a[i][wi]][hig] * w[(wi, low)] >= -ks * w[(wi, low)]
            )
        for i in range(1, len(a)):
            problem += w[(i, 1)] <= w[(i, 2)] <= w[(i, 3)]
        m1, m2, m3 = 1 / 6, 4 / 6, 1 / 6
        problem += (
            w[(1, 1)] * m1
            + w[(1, 2)] * m2
            + w[(1, 3)] * m3
            + w[(2, 1)] * m1
            + w[(2, 2)] * m2
            + w[(2, 3)] * m3
            + w[(3, 1)] * m1
            + w[(3, 2)] * m2
            + w[(3, 3)] * m3
            + w[(4, 1)] * m1
            + w[(4, 2)] * m2
            + w[(4, 3)] * m3
            == 1
        )

        problem.solve()
        ans = []
        for i in range(1, len(a)):
            ans.append(GMIR([w[(i, 1)], w[(i, 2)], w[(i, 3)]]))
        return np.array(ans)

    @staticmethod
    def __best_worst_method_get_weights():
        """
        a = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 4, 5],
            [0, 0, 1, 0, 3],
            [0, 0, 0, 1, 2],
            [0, 0, 0, 0, 1],
        ]
        """
        # 1. Delay 2.GPU 3.CPU 4.MEM
        a = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 3, 3],
            [0, 0, 1, 0, 2],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ]

        problem = LpProblem("BWM_Objective", LpMinimize)

        ks = LpVariable("ks", lowBound=0)
        w1 = LpVariable("w1", lowBound=0)
        w2 = LpVariable("w2", lowBound=0)
        w3 = LpVariable("w3", lowBound=0)
        w4 = LpVariable("w4", lowBound=0)
        # min ks
        problem += ks, "Objective"
        # |wB/wj - aBj| <= ks, for all j
        # |wj/wW - ajW| <= ks, for all j
        # problem += abs(w1/w2-a[1][2]) <= ks, "Constraint 1"
        # problem += abs(w1/w3-a[1][3]) <= ks, "Constraint 2"
        # problem += abs(w1/w4-a[1][4]) <= ks, "Constraint 3"
        # problem += abs(w2/w4-a[2][4]) <= ks, "Constraint 4"
        # problem += abs(w3/w4-a[3][4]) <= ks, "Constraint 5"
        for j, (wA, wB, aVal) in enumerate(
            [
                (w1, w2, a[1][2]),
                (w1, w3, a[1][3]),
                (w1, w4, a[1][4]),
                (w2, w4, a[2][4]),
                (w3, w4, a[3][4]),
            ],
            1,
        ):
            u = LpVariable(f"u{j}", lowBound=0)
            problem += wA - aVal * wB <= ks, f"Constraint {2*j-1}"
            problem += -wA + aVal * wB <= ks, f"Constraint {2*j}"
        # w1 + ... + wj == 1
        problem += w1 + w2 + w3 + w4 == 1, "Constraint sum1"

        problem.solve()
        return np.array([w1.value(), w2.value(), w3.value(), w4.value()])

    def __best_worst_method(self, node_ids, task) -> int:
        info = []
        ids = []
        for node_id in node_ids:
            node = self.cluster.node_list[node_id - 1]
            t = [
                1 / task.transmit_time,
                node.gpu_utilization,
                node.cpu_utilization,
                node.mem_utilization,
            ]
            info.append(t)
            ids.append(node.id)
        matrix = np.array(info)
        norm_matrix = self.normalize_matrix(matrix)
        weights = self.BWM_WEIGHT
        weights_matrix = norm_matrix * weights
        row_sums = np.sum(weights_matrix, axis=1)
        ids = np.array(ids)
        sorted_indices = np.argsort(row_sums)[::-1]
        sorted_ids = ids[sorted_indices]
        for node_id in ids:
            node = self.cluster.node_list[node_id - 1]
            ok, err = node.can_run_task(task)
            if ok:
                return node_id
        return -1

    def make_decision(self, task: Task, clock) -> int:
        group_id = self.__find_in_first_group(task)
        gid = group_id
        if gid == -1:
            # print("first-level, can not find any node can run the task:", task)
            return -1
        node_id = -1
        while gid <= util.GROUP_COUNT:
            node_ids = self.__find_in_second_group(
                gid, task, task.ai_accelerators is not None
            )
            if len(node_ids) == 0:
                # print("second-level group_id:{} can not find any node can run the task: {}".format(gid, task))
                gid += 1
                continue
            # node_id = self.__vikor(node_ids, task)
            node_id = self.__best_worst_method(node_ids, task)
            if node_id == -1:
                # print("second-level group_id:{} have not enough resource to run the task: {}".format(gid, task))
                gid += 1
            else:
                break
        """
        if gid > util.GROUP_COUNT: # cannot found any node has resrouce to process the task.
            gid = group_id
            while gid <= util.GROUP_COUNT:
                node_ids = self.__find_in_second_group(gid, task, False)
                if len(node_ids) == 0:
                    gid += 1
                    continue
                node_id = self.__best_worst_method(node_ids, task)
                if node_id == -1:
                    gid += 1
                else:
                    break
        """
        return node_id
