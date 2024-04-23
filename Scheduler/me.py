# Copyright 2024 The ScheduleSimPy Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/4 14:10
# Author  : linyf49@qq.com
# File    : me.py.py
"""
目标是什么：平均响应时间，负载均衡

数据密集型（Data-Intensive）：数据密集型任务是那些需要大量数据处理和存储的任务。
这些任务通常涉及大规模的数据集，例如数据分析、数据挖掘、机器学习等。
数据密集型任务的特点是对大量数据进行操作和分析，需要高效的数据处理和存储系统来处理大规模数据。
Rely: 高速内存RAM，高性能CPU，固态硬盘SSD，机械硬盘HDD，显卡GPU

IO密集型（IO-Intensive）：IO密集型任务是那些需要大量的输入输出操作的任务。
这些任务通常涉及到文件系统或网络的读写操作，例如文件传输、数据库查询、网络通信等。
IO密集型任务的特点是大量的数据读写操作，需要高效的IO系统来处理大量的IO请求。
Rely: 高速内存RAM，高性能CPU，固态硬盘SSD

网络密集型（Network-Intensive）：网络密集型任务是那些需要大量的网络通信的任务。
这些任务通常涉及到网络传输和通信，例如网站访问、实时视频流处理、分布式系统通信等。
网络密集型任务的特点是大量的网络数据传输和通信，需要高效的网络系统来处理大规模的网络请求和通信。
Rely: 高带宽网络接口

计算密集型（Compute-Intensive）：计算密集型任务是那些需要大量计算资源的任务。
这些任务通常涉及到大量的数学计算、算法运算和模型推理，例如科学计算、数值模拟、图像处理等。
计算密集型任务的特点是大量的数学计算和运算，需要高效的计算资源来进行处理和计算。
Rely: CPU, GPU

CPU(Central Processing Unit)
GPU(Graphics Processing Unit)
TPU(Tensor Processing Unit)
NPU(Neural network Processing Unit)


"""


from Scheduler.scheduler import Scheduler


class GroupBaseContainerScheduling(Scheduler):
    def __init__(self, name: str, env):
        super(GroupBaseContainerScheduling, self).__init__(name, env)

    def group(self):
        for node in self.cluster.node_list:
            pass
