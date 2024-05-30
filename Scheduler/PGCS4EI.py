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
from Scheduler.scheduler import Scheduler
from sklearn import preprocessing
from sklearn.cluster import KMeans


class GroupBaseContainerScheduling(Scheduler):
    def __init__(self, name: str, env):
        super(GroupBaseContainerScheduling, self).__init__(name, env)
        self.groups = dict()
        self.groups_min = dict()  # min(CPU,MEM) in one group

    def make_group(self):
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

        # 归一化处理
        scaler = preprocessing.MinMaxScaler()
        df[features] = scaler.fit_transform(df[features])

        k_optimal = 3
        # Custom K-means initial centroids.
        # custom_centroids = df_original.loc[[59, 89, 99], features].values
        # kmeans = KMeans(n_clusters=k_optimal, init=custom_centroids, n_init=1, random_state=42)
        kmeans = KMeans(n_clusters=k_optimal, random_state=42)
        df["group"] = kmeans.fit_predict(df[features])
        df_original["group"] = df["group"]
        for index, row in df_original.iterrows():
            # print(
            #     f"ID: {row['id']}, "
            #     f"CPU: {row['cpu']}, "
            #     f"Mem: {row['mem']}GB, "
            #     f"Disk: {row['disk']}GB, "
            #     f"Bandwidth: {row['band']}Mbps, "
            #     f"Group: {row['group']}"
            # )
            group_id = row["group"]
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
