# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/3/31 15:48
# Author  : linyf49@qq.com
# File    : odcs.py
# Paper   : Online Container Scheduling for Data-intensive Applications in Serverless Edge Computing
"""
伪代码
for i in I do
    G(i) = build_graph(i)
    for nk in N(data) do
        Dijkstra(nk)
    end for
    for n in N do
        h(i,n) = min(l(i,nk,n))
        a'(i,n) = a(i,n) + h(i,n)
    end for
    for n in N do
        if n == 1 then
            δ(i,n) = a'(i,n) + c(i) * p
        else if z(n) == 0 then
            δ(i,n) = a'(i,n) + γ(n)
        else
            δ(i,n) = a'(i,n)
        end if
        set = sort(δ(i,n))
        // Denote the current workload of node n is L(n).
        for n in set do
            if L(n) + c(i) <= C(n) then
                x(i,n) = 1
                L(n) = L(n) + c(i)
                y(i,nk) = 1, where l(i,nk,n) = h(i,n)
                if z(n) == 0 then
                    z(n) = 1
                end if
                f(i,n1,n2) = 1 along the shortest path from n(k) to n in G(i)
                Break
            end if
        end for
    end for
end for

算法流程：
1. 对于每一个待调度的容器 i，构造一个有向图 G(i)，
   图中边的权重为 w(i,n1,n2) 表示容器 i 及其数据源之间的数据流通过链路 e(n1,n2) 所产生的传输延迟
2. 对于所有拥有容器 i 执行所需数据的节点 nk，执行一次单源最短路径算法
   这就得出了节点 nk 达到其他所有节点的最短路 l(i,nk,n)
3. 对于每个节点 n，找出哪个拥有数据的节点nk离自己最近，然后计算出容器 i 在此节点上的总延迟 a'(i,n)（等于数据传输延迟+执行延迟）
   此时问题化简为 P2
4. 对于每个节点 n，计算增量 δ(i,n)
    4.1. 如果节点 n 为云节点， 则 δ(i,n) = a'(i,n) + c(i) * p
    4.2. 如果节点 n 为边缘节点，且没有部署无服务器应用，则 δ(i,n) = a'(i,n) + γ(n)
    4.3. 如果节点 n 为边缘节点，且已经部署无服务器应用，则 δ(i,n) = a'(i,n)
5. 根据增量大小排序，选择出增量最小且资源满足要求的节点作为调度节点，并更新相应状态
"""
from typing import List
from math import inf

from Scheduler.scheduler import Scheduler
from Infrastructure.cluster import Cluster, EdgeNode
from Task.task import Task


class OnlineContainerScheduling(Scheduler):
    def __init__(self, name: str, cluster: Cluster):
        super(OnlineContainerScheduling, self).__init__(name, cluster)
        self._cluster = cluster
        self._cloud_cost_p = 1  # 容器在云节点执行成本的固定系数
        self.n = self._cluster.get_node_num()
        self._serverless_z = [] * (self.n + 1)  # 边缘节点是否启动无服务器
        self._serverless_cost = [] * (self.n + 1)  # 边缘节点运营无服务器的成本
        self._mem_capacity = [] * (self.n + 1)  # 集群中每个节点的内存容量
        self._mem_used = [] * (self.n + 1)

    def __prepare(self):
        # 获取调度所需要的集群信息
        for node in self._cluster.node_list:
            self._mem_capacity[node.id] = node.mem_capacity

    def make_decision(self, task: Task) -> EdgeNode:
        n = self.n  # 节点数量
        g = [[inf] * n for _ in range(n)]  # 邻接矩阵建图
        for i in range(n):
            g[i][i] = 0
        for node in self._cluster.node_list:
            for edge in node.edges:
                g[node.id][edge[0]] = edge[1]

        def dijkstra(v: int) -> List[int]:
            done = set()  # 已找到最短路的节点集合
            dist = [inf] * n
            dist[v] = 0
            while len(done) < n:
                # 找到当前dist中的最小值
                x = -1
                for i in range(n):
                    if i in done:
                        continue
                    if x == -1 or dist[i] < dist[x]:
                        x = i
                done.add(x)
                # 更新dist数组
                for i in range(n):
                    if i not in done:
                        continue
                    if g[x][i] != inf and dist[x] + g[x][i] < dist[i]:
                        dist[i] = dist[x] + g[x][i]
            return dist

        l = dict()  # l[nk]维护节点nk的最短路数组
        for nk in n_data:
            # 对于所有拥有容器数据的节点执行一次最短路算法
            dist = dijkstra(nk)
            l[nk] = dist

        h = [(inf, -1)] * n  # h[i]维护nk到节点i的最小值，以及对应nk的编号
        for i in range(n):
            for nk in n_data:
                if l[nk][i] < h[i][0]:
                    h[i] = (l[nk][i], nk)
        # 将执行延迟和数据传输延迟合并成总延迟
        ap = [a[i] + h[i][0] for i in range(n)]

        # 计算将容器调度到节点 i 执行所产生的对目标函数P2的增量
        inc = [0.0] * n
        for i in range(n):
            if i == 0:  # 云节点
                inc[0] = ap[0] + c * p
            elif z[i] == 0:
                inc[i] = ap[i] + serverless_cost[i]
            else:
                inc[i] = ap[i]
        # 所有节点按照增量从小到大排序
        n_sort = sorted(zip(inc, range(n)))
        n_sort.sort(key=lambda xx: xx[0])

        x = [0] * n
        y = [0] * n
        f = [[0] * n for _ in range(n)]
        for t in n_sort:
            idx = t[1]
            if cur[idx] + c <= capacity[idx]:  # 满足执行要求
                # 选择第一个满足要求的idx作为调度节点
                x[idx] = 1
                cur[idx] += c
                # 标记容器数据从哪个点提取
                y[h[idx][1]] = 1
                # 节点idx没有启动serverless服务
                if z[idx] == 0:
                    z[idx] = 1
                # TODO Assign f[n1][n2] to 1 along the shortest path from nk to n in G.
                return idx
