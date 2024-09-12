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
import random

from Scheduler.scheduler import Scheduler
from Task.task import Task


class OnlineContainerScheduling(Scheduler):
    def __init__(self, name: str, env):
        super(OnlineContainerScheduling, self).__init__(name, env)

    def make_decision(self, task: Task, clock) -> int:
        # prepare
        n = self.cluster.node_num
        scores = [0] * n
        ids = [i for i in range(n)]
        for i, node in enumerate(self.cluster.node_list):
            addition_time = 1
            if not node.gpu_match(task):
                addition_time = 3.6
            delay = addition_time * task.duration
            scores[i] = delay + random.randint(0, 1) * random.uniform(0, 0)
        ids.sort(key=lambda i: scores[i])
        for idx in ids:
            ok, err = self.cluster.node_list[idx].can_run_task(task)
            if ok:
            # if ok and self.cluster.node_list[idx].gpu_match(task):
                return idx + 1
        return -1
